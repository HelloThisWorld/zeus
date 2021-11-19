import json

from thunder.model.Package import Package
from thunder.servcie import BASE_URL
from thunder.util.HttpClientUtil import fetch_content_from_tar


class PackageContentService:
    def __init__(self, _conn):
        self.conn = _conn

    def build_packages(self, txt_arr: list) -> list:
        """
        This function generate a list of packages
        Only the will format and valid packages will be returned
        """
        package_list = list()
        for item in txt_arr:
            item_arr = item.split("\n")
            for param in item_arr:
                pack_name = PackageContentService._get_param_value(param=param, start_with="Package:")
                if pack_name:
                    break

            for param in item_arr:
                version = PackageContentService._get_param_value(param=param, start_with="Version:")
                if version:
                    break

            if pack_name and version:
                package = Package(pack_name=pack_name, version=version)
                package_list.append(package)

        return package_list

    def batch_insert_data(self, packages: list, force_insert: bool = False):
        count = self.conn.count()
        if count <= 1000 or force_insert:
            for item in packages:
                if self._save_one_to_db(item=item):
                    print(f"{item.get('pack_name')} saved")
                else:
                    print(f"{item.get('pack_name')} save failed")
        else:
            print(f"No data inserted as collection already contains {count} items")

    def enriched_packages(self, package: Package):
        package_description = fetch_content_from_tar(url=f"{BASE_URL}/{package.get_tar_name()}")
        description_map = PackageContentService._description_to_dict(description=package_description)
        if "Date/Publication" in description_map:
            package.set("Date/Publication", description_map.get("Date/Publication"))

        if "Title" in description_map:
            package.set("Title", description_map.get("Title"))

        if "Description" in description_map:
            package.set("Description", description_map.get("Description"))

        if "Author" in description_map:
            package.set("Author", description_map.get("Author"))

        if "Maintainer" in description_map:
            maintainer = description_map.get("Maintainer")
            package.set("Maintainer", description_map.get("Maintainer"))
            # e.g. Scott Fortmann-Roe <scottfr@berkeley.edu>
            # After split should be
            # Name: Scott Fortmann-Roe
            # Email: scottfr@berkeley.edu>
            name_email_arr = maintainer.split("<")
            package.set("Name", name_email_arr[0].strip())
            # Remove the last ">" in the Email e.g. scottfr@berkeley.edu>
            package.set("Email", name_email_arr[1][:-1].strip())

    def fetch_by_name(self, pack_name: str) -> dict:
        try:
            pack = self.conn.find_one({"pack_name": pack_name})
            if not pack:
                return {"error": f"No result for package name '{pack_name}'"}

            # If content not enriched, do enriched from DESCRIPTION file from tar
            if len(pack) < 4:
                package = Package(pack_name=pack["pack_name"], version=pack["version"])
                self.enriched_packages(package)
                self.conn.update({'_id': pack["_id"]},  {'$set': package.to_dict()})

            pack = self.conn.find_one({"pack_name": pack_name})
            # Remove the generated ID
            del pack["_id"]
            return pack
        except Exception as e:
            # Other errors are possible, such as IOError.
            print(f"Error: {str(e)}")
            return None

    @staticmethod
    def _description_to_dict(description: str) -> dict:
        result = dict()
        description_arr = description.split("\n")
        for item in description_arr:
            if ":" in item:
                k_v = item.split(":")
                result[k_v[0].strip()] = k_v[1].strip()

        return result

    def _save_one_to_db(self, item: Package) -> bool:
        try:
            self.conn.update({"pack_name": item.get("pack_name")}, {"$set": item.to_dict()}, upsert=True)
        except Exception as e:
            # Other errors are possible, such as IOError.
            print(f"Error: {str(e)}")
            return False

        return True

    @staticmethod
    def _get_param_value(param: str, start_with: str) -> str:
        if param.startswith(start_with):
            value = param.split(":")[1].strip()
        else:
            value = None

        return value

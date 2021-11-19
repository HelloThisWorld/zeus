from thunder.servcie.PackageContentService import PackageContentService
from thunder.util.DBConnectionUtil import get_connection
from thunder.util.HttpClientUtil import fetch_data, fetch_content_from_tar

BASE_URL = "http://cran.r-project.org/src/contrib"


def load_data():
    """
    This function is using to connect remote data source to retrieve data
    """
    try:
        conn = get_connection()
        package_service = PackageContentService(conn)
        # Data source from R package lib
        response = fetch_data(url=f"{BASE_URL}/PACKAGES")
        # Response body length is about 4MB, cloud be directly proceed
        txt = response.body.decode(encoding='utf-8')
        # Response data format is plaint text with empty lines
        txt_arr = txt.split('\n\n')
        packages = package_service.build_packages(txt_arr=txt_arr)
        # Insert the packages to DB
        package_service.batch_insert_data(packages=packages)
    except Exception as e:
        # Other errors are possible, such as IOError.
        print(f"Error: {str(e)}")


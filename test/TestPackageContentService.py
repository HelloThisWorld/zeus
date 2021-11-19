from unittest.mock import patch, Mock

from test import load_test_file
from thunder.model.Package import Package
from thunder.servcie.PackageContentService import PackageContentService


class TestPackageContentService:
    def test_build_packages_with_happy_path(self):
        # prepare
        _input = load_test_file("dummy_packages.txt")

        # action
        result = PackageContentService(Mock()).build_packages(_input.split("\n\n"))

        # assertion
        assert len(result) is 2
        assert result[0].get("pack_name") == "A3"
        assert result[0].get("version") == "1.0.0"
        assert result[0].get_tar_name() == "A3_1.0.0.tar.gz"
        assert result[1].get("pack_name") == "aaSEA"
        assert result[1].get("version") == "1.1.0"
        assert result[1].get_tar_name() == "aaSEA_1.1.0.tar.gz"

    def test_build_packages_with_missing_pack_name_data(self):
        # prepare
        _input = load_test_file("dummy_packages_with_error_fields.txt")

        # action
        result = PackageContentService(Mock()).build_packages(_input.split("\n\n"))

        # assertion
        assert len(result) is 2
        assert result[0].get("pack_name") == "abbyyR"
        assert result[0].get("version") == "0.5.5"
        assert result[0].get_tar_name() == "abbyyR_0.5.5.tar.gz"
        assert result[1].get("pack_name") == "abc.data"
        assert result[1].get("version") == "1.0"
        assert result[1].get_tar_name() == "abc.data_1.0.tar.gz"

    @patch("thunder.util.HttpClientUtil.fetch_content_from_tar")
    def test_enriched_packages(self, fetch_content_from_tar):
        # prepare
        mock_result = load_test_file("dummy_description.txt")
        fetch_content_from_tar.return_value = mock_result

        package = Package(pack_name="A3", version="1.0.0")

        # action
        PackageContentService(Mock()).enriched_packages(package=package)

        # assertion
        assert package.get("Email") == "scottfr@berkeley.edu"

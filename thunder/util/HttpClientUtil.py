import os
from tornado import httpclient
from tornado.httpclient import HTTPResponse, HTTPRequest
import tarfile
import requests


ME = __file__
ROOT_DIR = os.path.dirname(os.path.abspath(ME + "/../../"))


def fetch_data(url: str, method: str = 'GET') -> HTTPResponse:
    try:
        request = HTTPRequest(url=url, method=method)

        http_client = httpclient.HTTPClient()
        response = http_client.fetch(request)

        return response
    except httpclient.HTTPError as e:
        # HTTPError is raised for non-200 responses; the response
        # can be found in e.response.
        print(f"Error: {str(e)}")
    except Exception as e:
        # Other errors are possible, such as IOError.
        print(f"Error: {str(e)}")
    finally:
        http_client.close()


def fetch_content_from_tar(url: str, file_name: str = "DESCRIPTION") -> str:
    base_path = url.split("/")[-1].split("_")[0]
    member_path = f"{base_path}/{file_name}"

    target_path = f'{ROOT_DIR}/thunder/temp.tar.gz'

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(target_path, 'wb') as f:
            f.write(response.raw.read())
            f.close()

    tar = tarfile.open(target_path)
    if tar.getmember(member_path):
        member = tar.getmember(member_path)
        f = tar.extractfile(member)
        f_content = f.read().decode()
        f.close()
    else:
        f_content = None
    tar.close()

    # Remove temp file
    if os.path.exists(target_path):
        os.remove(target_path)
        print(f"{file_name} file processed")
    else:
        print("The file does not exist")

    return f_content

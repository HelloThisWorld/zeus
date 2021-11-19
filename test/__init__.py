import os

ME = __file__
ROOT_DIR = os.path.dirname(os.path.abspath(ME + "/../"))


def load_test_file(file_name) -> str:
    path = f"{ROOT_DIR}/test/dummy_data/{file_name}"
    with open(path, encoding='utf-8') as data:
        return data.read()

import yaml

from common.settings import FILE_PATH


class Utils:
    @staticmethod
    def get_extract_data(extract_key: str):
        with open(FILE_PATH["EXTRACT"], "r") as f:
            data = yaml.safe_load(f)
        for item in data:
            if extract_key in item.keys():
                return item[extract_key]
        return None
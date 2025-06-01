import json
import jsonpath


def extract_response(extract: dict, response: dict):
    extracted_data = {}
    for key, pattern in extract.items():
        if "$" in pattern:
            value = jsonpath.jsonpath(response, pattern)
            if value:
                extracted_data[key] = value[0]
            else:
                extracted_data[key] = "No data extracted"
        else:
            raise NotImplementedError
    return extracted_data
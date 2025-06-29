import json
import traceback

import allure

from json.decoder import JSONDecodeError
from common.settings import URL_HOST, FILE_PATH
from test_framework.core.read_yaml import resolve_placeholder, write_yaml
from test_framework.core.send_request import send_request
from test_framework.core.extract_response import extract_response
from test_framework.core.assertions import assert_result
from test_framework.core.logger import logger


def run_testcase(testcase: dict):
    allowed_request_type = ["data", "json"]

    try:
        api_name = testcase["api_name"]
        allure.attach(f"API: {api_name}", "Testcase Info", allure.attachment_type.TEXT)

        endpoint = resolve_placeholder(testcase["url"])
        url = URL_HOST + endpoint
        allure.attach(f"URL: {url}", "Testcase Info", allure.attachment_type.TEXT)

        method = testcase["method"]
        allure.attach(f"Method: {method}", "Testcase Info", allure.attachment_type.TEXT)

        header = resolve_placeholder(testcase["header"])
        allure.attach(f"Header: {header}", "Testcase Info", allure.attachment_type.TEXT)

        case_name = testcase["case_name"]
        allure.attach(f"Case: {case_name}", "Testcase Info", allure.attachment_type.TEXT)

        request_kwargs = {}
        for request_type in allowed_request_type:
            if request_type in testcase:
                request_params = resolve_placeholder(testcase[request_type])
                request_kwargs = {request_type: request_params}

        request_kwargs_text = json.dumps(request_kwargs)
        allure.attach(f"Params: {request_kwargs_text}", "Testcase Info", allure.attachment_type.TEXT)

        validation = resolve_placeholder(testcase["validation"])
        extract = resolve_placeholder(testcase.get("extract", {}))

        response = send_request(
            url=url, header=header, method=method,
            **request_kwargs
        )
        status_code = response.status_code

        try:
            response_json = response.json()
            
            response_text = json.dumps(response_json, indent=4)
            allure.attach(response_text, "Response", allure.attachment_type.TEXT)
            
            if extract:
                extracted_data = extract_response(extract, response_json)
                write_yaml(FILE_PATH["EXTRACT"], extracted_data)
            
            assert_result(validation, response_json, status_code)
        except JSONDecodeError as e:
            logger.error("Response is not a valid JSON")
            raise e
        except Exception as e:
            logger.error(e)
            raise e
    
    except Exception as e:
        raise e
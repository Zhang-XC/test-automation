import json

import allure

from test_framework.core.logger import logger


def assert_result(validation: list, response: dict, status_code: int):
    n_failed_cases = 0
    for val in validation:
        key = list(val.keys())[0]
        if key == "status":
            n_failed_cases += assert_equal(val, {"status": status_code})
        elif key == "eq":
            n_failed_cases += assert_equal(val[key], response)
        elif key == "neq":
            n_failed_cases += assert_not_equal(val[key], response)
        elif key == "contains":
            n_failed_cases += assert_contains(val[key], response)
        else:
            raise NotImplementedError

    if n_failed_cases != 0:
        logger.error("One or more assertions failed")
        assert False
    else:
        logger.info("All assertions passed")


def assert_equal(expected_output: dict, response: dict):
    if not (isinstance(expected_output, dict) and isinstance(response, dict)):
        raise TypeError
    
    actual_output = {key: response[key] for key in expected_output}
    if expected_output == actual_output:
        failed = 0
        allure.attach(
            f"Assertion passed\nExpected: {expected_output}\nActual: {actual_output}",
            name=f"Equality assertion", attachment_type=allure.attachment_type.TEXT
        )
    else:
        failed = 1
        allure.attach(
            f"Assertion failed\nExpected: {expected_output}\nActual: {actual_output}",
            name="Equality assertion", attachment_type=allure.attachment_type.TEXT
        )
    return failed


def assert_not_equal(expected_output: dict, response: dict):
    if not (isinstance(expected_output, dict) and isinstance(response, dict)):
        raise TypeError

    actual_output = {key: response[key] for key in expected_output}
    if expected_output != actual_output:
        failed = 0
        allure.attach(
            f"Assertion passed\nExpected: {expected_output}\nActual: {actual_output}",
            name="Inequality assertion", attachment_type=allure.attachment_type.TEXT
        )
    else:
        failed = 1
        allure.attach(
            f"Assertion failed\nExpected: {expected_output}\nActual: {actual_output}",
            name="Inequality assertion", attachment_type=allure.attachment_type.TEXT
        )
    return failed


def assert_contains(expected_output: dict, response: dict):
    if not (isinstance(expected_output, dict) and isinstance(response, dict)):
        raise TypeError
    
    failed = 0
    for key in expected_output.keys():
        if expected_output[key] not in response[key]:
            failed = 1

    actual_output = {key: response[key] for key in expected_output}
    if failed == 0:
        allure.attach(
            f"Assertion passed\nExpected: {expected_output}\nActual: {actual_output}",
            name="Containment assertion", attachment_type=allure.attachment_type.TEXT
        )
    else:
        allure.attach(
            f"Assertion failed\nExpected: {expected_output}\nActual: {actual_output}",
            name="Containment assertion", attachment_type=allure.attachment_type.TEXT
        )
    return failed
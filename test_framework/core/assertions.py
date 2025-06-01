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
    
    n_failed_cases = 0
    for key in expected_output.keys():
        if expected_output[key] == response[key]:
            allure.attach(
                f"Assertion passed for key: {key}\nExpected: {expected_output[key]}\nActual: {response[key]}",
                name=f"Equality assertion", attachment_type=allure.attachment_type.TEXT
            )
        else:
            n_failed_cases += 1
            allure.attach(
                f"Assertion failed for key: {key}\nExpected: {expected_output[key]}\nActual: {response[key]}",
                name="Equality assertion", attachment_type=allure.attachment_type.TEXT
            )
    return n_failed_cases


def assert_not_equal(expected_output: dict, response: dict):
    if not (isinstance(expected_output, dict) and isinstance(response, dict)):
        raise TypeError
    
    n_failed_cases = 0
    for key in expected_output.keys():
        if expected_output[key] != response[key]:
            allure.attach(
                f"Assertion passed for key: {key}\nExpected: {expected_output[key]}\nActual: {response[key]}",
                name="Inequality assertion", attachment_type=allure.attachment_type.TEXT
            )
        else:
            n_failed_cases += 1
            allure.attach(
                f"Assertion failed for key: {key}\nExpected: {expected_output[key]}\nActual: {response[key]}",
                name="Inequality assertion", attachment_type=allure.attachment_type.TEXT
            )
    return n_failed_cases


def assert_contains(expected_output: dict, response: dict):
    if not (isinstance(expected_output, dict) and isinstance(response, dict)):
        raise TypeError
    
    n_failed_cases = 0
    for key in expected_output.keys():
        if str(expected_output[key]) in str(response[key]):
            allure.attach(
                f"Assertion passed for key: {key}\nExpected: {expected_output[key]}\nActual: {response[key]}",
                name="Containment assertion", attachment_type=allure.attachment_type.TEXT
            )
        else:
            n_failed_cases += 1
            allure.attach(
                f"Assertion failed for key: {key}\nExpected: {expected_output[key]}\nActual: {response[key]}",
                name="Containment assertion", attachment_type=allure.attachment_type.TEXT
            )
    return n_failed_cases
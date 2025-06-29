import allure
import pytest

from test_framework.core.read_yaml import load_testcase
from test_framework.core.generate_id import m_id, c_id, generate_order
from test_framework.core.run_testcase import run_testcase


order = generate_order()


@allure.feature(next(m_id) + "User Management")
class TestUserManager:
    @allure.story(next(c_id) + "Register")
    @pytest.mark.run(order=next(order))
    @pytest.mark.parametrize("testcase", load_testcase("test_register_user.yaml"))
    def test_register(self, testcase):
        allure.dynamic.title(testcase['case_name'])
        run_testcase(testcase)

    @allure.story(next(c_id) + "Login")
    @pytest.mark.run(order=next(order))
    @pytest.mark.parametrize("testcase", load_testcase("test_login.yaml"))
    def test_login(self, testcase):
        allure.dynamic.title(testcase['case_name'])
        run_testcase(testcase)

    @allure.story(next(c_id) + "Delete")
    @pytest.mark.run(order=next(order))
    @pytest.mark.parametrize("testcase", load_testcase("test_delete_user.yaml"))
    def test_delete_user(self, testcase):
        allure.dynamic.title(testcase['case_name'])
        run_testcase(testcase)
import allure
import pytest

from test_framework.core.read_yaml import load_testcase
from test_framework.core.generate_id import m_id, c_id
from test_framework.core.run_testcase import run_testcase


@allure.feature(next(m_id) + "User Management")
class TestUserManager:
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize("testcase", load_testcase("test_register.yaml"))
    def test_register(self, testcase):
        allure.dynamic.title(testcase['case_name'])
        run_testcase(testcase)

    @pytest.mark.run(order=2)
    @pytest.mark.parametrize("testcase", load_testcase("test_login.yaml"))
    def test_login(self, testcase):
        allure.dynamic.title(testcase['case_name'])
        run_testcase(testcase)
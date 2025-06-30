import allure
import pytest

from test_framework.core.read_yaml import load_testcase
from test_framework.core.generate_id import m_id, c_id, generate_order
from test_framework.core.run_testcase import run_testcase


order = generate_order()


@allure.feature(next(m_id) + "Cart Management")
class TestProductManager:
    @allure.story(next(c_id) + "Cart items")
    @pytest.mark.run(order=next(order))
    @pytest.mark.parametrize("testcase", load_testcase("test_cart.yaml"))
    def test_login(self, testcase):
        allure.dynamic.title(testcase['case_name'])
        run_testcase(testcase)
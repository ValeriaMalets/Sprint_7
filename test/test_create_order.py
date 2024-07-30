import allure
import pytest
from src.data import SCOOTER_COLOR, ORDER_DATA
from test.helpers import OrderHelper


@allure.feature("Orders")
class TestCreateOrder:

    @allure.story("Creating an order with different scooter color options")
    @pytest.mark.parametrize('color', SCOOTER_COLOR)
    def test_create_order(self, color):
        payload = ORDER_DATA.copy()  # Copying order data
        payload["color"] = color

        allure.step("Creating an order")
        response = OrderHelper.create_order(payload)

        allure.step("Checking that the order was created successfully")
        assert response.status_code == 201

        allure.step("Checking that the response contains a track number")
        response_data = response.json()
        assert 'track' in response_data

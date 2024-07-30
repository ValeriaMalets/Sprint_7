import allure
from test.helpers import OrderHelper


@allure.feature("Orders")
class TestOrderList:

    @allure.story("Retrieving active and completed courier orders")
    def test_get_orders_list(self):
        response = OrderHelper.get_orders()

        allure.step("Checking response status")
        assert response.status_code == 200
        response_data = response.json()

        allure.step("Checking for orders in the response")
        assert 'orders' in response_data
        assert isinstance(response_data['orders'], list)
        assert len(response_data['orders']) > 0

        for order in response_data['orders']:
            OrderHelper.assert_order_structure(order)

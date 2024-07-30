import unittest
import allure

from test.helpers import CourierHelper
from src.utils import register_new_courier_and_return_login_password
from src.error_messages import INSUFFICIENT_DATA_FOR_LOGIN, ACCOUNT_NOT_FOUND


@allure.feature("Courier Login")
class CourierLoginTest(unittest.TestCase):
    @allure.story("Courier can login successfully")
    @allure.step("Test courier can login successfully")
    def test_courier_can_login_successfully(self):
        allure.dynamic.description("Register a new courier and verify the login is successful.")
        login_pass = register_new_courier_and_return_login_password()
        payload = {
            "login": login_pass[0],
            "password": login_pass[1]
        }
        response = CourierHelper.login_courier(payload)
        print(f"Login response: {response.status_code}, {response.json()}")  # Debug information
        self.assertEqual(response.status_code, 200)
        self.assertIn("id", response.json())

    @allure.story("Login requires all fields")
    @allure.step("Test login requires all fields")
    def test_login_requires_all_fields(self):
        allure.dynamic.description("Send a login request with empty login and password and verify the response.")
        payload = {
            "login": "",
            "password": ""
        }
        response = CourierHelper.login_courier(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("message", response.json())
        self.assertEqual(response.json()["message"], INSUFFICIENT_DATA_FOR_LOGIN)

    @allure.story("Login with empty password")
    @allure.step("Test login with empty password")
    def test_login_with_empty_password(self):
        allure.dynamic.description("Register a new courier and send a login request with an empty password.")
        login_pass = register_new_courier_and_return_login_password()
        payload = {
            "login": login_pass[0],
            "password": ""
        }
        response = CourierHelper.login_courier(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("message", response.json())
        self.assertEqual(response.json()["message"], INSUFFICIENT_DATA_FOR_LOGIN)

    @allure.story("Login with empty login")
    @allure.step("Test login with empty login")
    def test_login_with_empty_login(self):
        allure.dynamic.description("Register a new courier and send a login request with an empty login.")
        login_pass = register_new_courier_and_return_login_password()
        payload = {
            "login": "",
            "password": login_pass[1]
        }
        response = CourierHelper.login_courier(payload)
        print(f"Response for empty login: {response.status_code}, {response.json()}")  # Debug information
        self.assertEqual(response.status_code, 400)
        self.assertIn("message", response.json())
        self.assertEqual(response.json()["message"], INSUFFICIENT_DATA_FOR_LOGIN)

    @allure.story("Login with only password")
    @allure.step("Test login with only password")
    def test_login_with_only_password(self):
        allure.dynamic.description("Register a new courier and send a login request with only the password.")
        login_pass = register_new_courier_and_return_login_password()
        payload = {
            "password": login_pass[1]
        }
        response = CourierHelper.login_courier(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("message", response.json())
        self.assertEqual(response.json()["message"], INSUFFICIENT_DATA_FOR_LOGIN)

    @allure.story("Login with non-existent user")
    @allure.step("Test login with non-existent user")
    def test_login_with_non_existent_user(self):
        allure.dynamic.description("Send a login request with non-existent user credentials and verify the response.")
        payload = {
            "login": "nonexistentuser",
            "password": "somepassword"
        }
        response = CourierHelper.login_courier(payload)
        print(f"Response for non-existent user login: {response.status_code}, {response.json()}")  # Debug information
        self.assertEqual(response.status_code, 404)
        self.assertIn("message", response.json())
        self.assertEqual(response.json()["message"], ACCOUNT_NOT_FOUND)


if __name__ == '__main__':
    unittest.main()

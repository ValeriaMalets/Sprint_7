import unittest
import allure

from test.helpers import CourierHelper
from src.utils import register_new_courier_and_return_login_password
from src.error_messages import LOGIN_ALREADY_EXISTS, INSUFFICIENT_DATA


@allure.feature("Courier")
class CourierTest(unittest.TestCase):
    @allure.story("Create courier successfully")
    @allure.step("Create a new courier successfully")
    def test_create_courier_successfully(self):
        allure.dynamic.description("Generate courier data and send a request to create a new courier.")
        payload = CourierHelper.generate_courier_data()
        response = CourierHelper.create_courier(payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"ok": True})

    @allure.story("Cannot create duplicate courier")
    @allure.step("Test creating a duplicate courier")
    def test_cannot_create_duplicate_courier(self):
        allure.dynamic.description("Register a new courier and attempt to create a duplicate courier.")
        login_pass = register_new_courier_and_return_login_password()
        payload = {
            "login": login_pass[0],
            "password": login_pass[1],
            "firstName": login_pass[2]
        }
        response_duplicate = CourierHelper.create_courier(payload)
        self.assertEqual(response_duplicate.status_code, 409)

    @allure.story("Conflict message for duplicate login")
    @allure.step("Test conflict message for duplicate login")
    def test_conflict_message_for_duplicate_login(self):
        allure.dynamic.description(
            "Register a new courier and verify the conflict message when creating a duplicate courier.")
        login_pass = register_new_courier_and_return_login_password()
        payload = {
            "login": login_pass[0],
            "password": login_pass[1],
            "firstName": login_pass[2]
        }
        response_duplicate = CourierHelper.create_courier(payload)
        self.assertEqual(response_duplicate.status_code, 409)
        self.assertIn("message", response_duplicate.json())
        self.assertEqual(response_duplicate.json()["message"], LOGIN_ALREADY_EXISTS)

    @allure.story("All fields required for courier creation")
    @allure.step("Test that all fields are required for courier creation")
    def test_all_fields_required(self):
        allure.dynamic.description(
            "Generate courier data and verify that all fields are required for courier creation.")
        payload = CourierHelper.generate_courier_data()
        for field in ['login', 'password']:
            invalid_payload = payload.copy()
            del invalid_payload[field]
            response = CourierHelper.create_courier(invalid_payload)
            print(f"Response for missing field {field}: {response.status_code}, {response.json()}")
            self.assertEqual(response.status_code, 400)
            self.assertIn("message", response.json())
            self.assertEqual(response.json()["message"], INSUFFICIENT_DATA)

        invalid_payload = payload.copy()
        del invalid_payload['firstName']
        response = CourierHelper.create_courier(invalid_payload)
        print(f"Response for missing field firstName: {response.status_code}, {response.json()}")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"ok": True})

    @allure.story("Correct response for missing fields")
    @allure.step("Test correct response for missing fields")
    def test_correct_response_for_missing_fields(self):
        allure.dynamic.description("Send a create courier request with an empty login and verify the response.")
        response = CourierHelper.create_courier({"login": "", "password": "test", "firstName": "test"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("message", response.json())
        self.assertEqual(response.json()["message"], INSUFFICIENT_DATA)


if __name__ == '__main__':
    unittest.main()

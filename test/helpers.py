from faker import Faker
import requests
from config import BASE_URL, COURIER_URL, ORDERS_URL
from src.utils import register_new_courier_and_return_login_password

fake = Faker()


class CourierHelper:
    @staticmethod
    def generate_courier_data():
        return {
            "login": fake.user_name(),
            "password": fake.password(),
            "firstName": fake.first_name()
        }

    @staticmethod
    def create_courier(payload):
        return requests.post(COURIER_URL, json=payload, timeout=10)

    @staticmethod
    def generate_payload_from_registered_courier():
        login_pass = register_new_courier_and_return_login_password()
        return {
            "login": login_pass[0],
            "password": login_pass[1],
            "firstName": login_pass[2]
        }

    @staticmethod
    def login_courier(payload):
        return requests.post(f"{BASE_URL}/courier/login", json=payload, timeout=10)


class OrderHelper:
    @staticmethod
    def create_order(payload):
        return requests.post(ORDERS_URL, json=payload, headers={"Content-Type": "application/json"})

    @staticmethod
    def get_orders(courier_id=None, nearest_station=None, limit=30, page=0):
        params = {
            "courierId": courier_id,
            "nearestStation": nearest_station,
            "limit": limit,
            "page": page
        }
        response = requests.get(ORDERS_URL, params=params)
        return response

    @staticmethod
    def assert_order_structure(order):
        expected_keys = [
            'id', 'courierId', 'firstName', 'lastName', 'address',
            'metroStation', 'phone', 'rentTime', 'deliveryDate',
            'track', 'color', 'comment', 'createdAt', 'updatedAt', 'status'
        ]
        for key in expected_keys:
            assert key in order, f"Missing key: {key}"

import json
import http.client
import sys
import unittest
from unittest.mock import MagicMock, patch
from io import StringIO


def make_request(method, path, headers, body=None):
    conn = http.client.HTTPSConnection("dummyjson.com")
    conn.request(method, path, body, headers)
    response = conn.getresponse()
    data = response.read().decode()
    conn.close()
    return response.status, data


def login(username, password):
    payload = json.dumps({
        "username": username,
        "password": password
    })

    headers = {
        "Content-Type": "application/json",
        "Cookie": "accessToken=tokenLogin"
    }

    status, data = make_request("POST", "/auth/login", headers, payload)

    if status != 200:
        print(f"Login failed: {status}")
        return None, None

    response_data = json.loads(data)
    access_token = response_data.pop("token", None) or response_data.pop("accessToken", None)
    response_data.pop("refreshToken", None)
    return access_token, response_data


def handle_authenticated_requests(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # GET /auth/me
    status_auth, data_auth = make_request("GET", "/auth/me", headers)

    # PUT /todos/2
    put_payload = json.dumps({"completed": False})
    status_update, data_update = make_request("PUT", "/todos/2", headers, put_payload)
    data_update = json.loads(data_update)

    # DELETE /todos/1
    status_delete, data_delete = make_request("DELETE", "/todos/1", headers)
    data_delete = json.loads(data_delete)

    return status_auth, status_update, data_update, status_delete, data_delete


class NullWriter(StringIO):
    def write(self, txt):
        pass


def assert_equal(parameter1, parameter2):
    if parameter1 == parameter2:
        print(f"test attribute passed: {parameter1} is equal to {parameter2}")
    else:
        print(f"test attribute failed: {parameter1} is not equal to {parameter2}")


class TestFetchUserInfo(unittest.TestCase):
    @patch("http.client.HTTPSConnection")
    def test_login_and_requests(self, MockHTTPSConnection):
        mock_response_login = MagicMock()
        mock_response_login.status = 200
        mock_response_login.read.return_value = json.dumps({
            "id": 1,
            "firstName": "Emily",
            "lastName": "Johnson",
            "email": "emily.johnson@x.dummyjson.com",
            "gender": "female",
            "image": "https://dummyjson.com/icon/emilys/128",
            "accessToken": "dummyAccessToken"
        }).encode("utf-8")

        mock_response_rest = MagicMock()
        mock_response_rest.status = 200
        mock_response_rest.read.return_value = b"{}"

        mock_response_put = MagicMock()
        mock_response_put.status = 200
        mock_response_put.read.return_value = json.dumps({
            "id": 2,
            "todo": "Memorize a poem",
            "completed": False,
            "userId": 13
        }).encode("utf-8")

        mock_response_delete = MagicMock()
        mock_response_delete.status = 200
        mock_response_delete.read.return_value = json.dumps({
            "id": 1,
            "todo": "Do something nice for someone you care about",
            "completed": False,
            "userId": 152,
            "isDeleted": True,
            "deletedOn": "2025-05-04T20:03:04.833Z"
        }).encode("utf-8")

        MockHTTPSConnection.return_value.getresponse.side_effect = [
            mock_response_login,
            mock_response_rest,
            mock_response_put,
            mock_response_delete
        ]

        access_token, user_data = login("emilys", "emilyspass")
        status_auth, status_update, data_update, status_delete, data_delete = (
            handle_authenticated_requests(access_token)
        )

        for conn_call in MockHTTPSConnection.call_args_list:
            args, kwargs = conn_call
            assert args[0] == "dummyjson.com"
        print(f"connection called with: {MockHTTPSConnection.call_args}")

        self.assertEqual(status_auth, 200)
        print("✅ GET /auth/me")

        assert_equal(user_data["id"], 1)
        assert_equal(user_data["firstName"], "Emily")
        assert_equal(user_data["lastName"], "Johnson")
        assert_equal(user_data["email"], "emily.johnson@x.dummyjson.com")
        assert_equal(user_data["gender"], "female")
        assert_equal(user_data["image"], "https://dummyjson.com/icon/emilys/128")

        self.assertEqual(status_update, 200)
        print("✅ PUT /todos/2 passed")

        assert_equal(data_update["id"], 2)
        assert_equal(data_update["todo"], "Memorize a poem")
        assert_equal(data_update["completed"], False)

        self.assertEqual(status_delete, 200)
        print("✅ DELETE /todos/1 passed")

        assert_equal(data_delete["id"], 1)
        assert_equal(data_delete["todo"], "Do something nice for someone you care about")
        assert_equal(data_delete["completed"], False)

    @patch("http.client.HTTPSConnection")
    def test_login_failure_400(self, MockHTTPSConnection):
        mock_response_400 = MagicMock()
        mock_response_400.status = 400
        mock_response_400.read.return_value = b'{"message": "Bad Request"}'

        MockHTTPSConnection.return_value.getresponse.return_value = mock_response_400

        original_stdout = sys.stdout
        sys.stdout = NullWriter()

        access_token, user_data = login("invalid_user", "invalid_pass")

        sys.stdout = original_stdout

        self.assertIsNone(access_token)
        self.assertIsNone(user_data)
        print("✅ test_login_failure_400: handled 400 Bad Request correctly")


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "run":
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        access_token, user_data = login(username, password)

        if access_token is None:
            print("Login failed, cannot proceed with authenticated requests.")
        else:
            status_auth, status_update, data_update, status_delete, data_delete = (
                handle_authenticated_requests(access_token)
            )

            print("Login :", access_token)
            print("User :", user_data)
            print("Auth :", status_auth)
            print("Update :", status_update)
            print("Update Data :", data_update)
            print("Delete :", status_delete)
            print("Delete Data :", data_delete)
    else:
        runner = unittest.TextTestRunner(stream=NullWriter())
        unittest.main(testRunner=runner, exit=False)

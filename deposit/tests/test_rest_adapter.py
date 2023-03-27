from unittest import TestCase
import requests
import mock
from deposit.rest_adapter import RestAdapter
from deposit.models import Response
from deposit.exceptions import DepositApiException


class TestRestAdapter(TestCase):
    def setUp(self) -> None:
        self.rest_adapter = RestAdapter("http://localhost")
        self.response = requests.Response()
        self.response.status_code = 200
        self.response._content = "{}".encode()
        self.deposit_response = Response(status_code=200)

    def test_do_successful_request(self):
        with mock.patch("requests.request", return_value=self.response):
            result = self.rest_adapter._do('GET', '')
        self.assertIsInstance(result, Response)
        self.assertEqual(result.status_code, 200)

    def test_do_unsuccessful_request(self):
        self.response.status_code = 404
        self.response._content = '{"error": "Not found"}'.encode()
        with mock.patch("requests.request", return_value=self.response):
            with self.assertRaises(DepositApiException):
                self.rest_adapter._do('GET', '')

    def test_do_bad_json_response(self):
        self.response._content = "Not a JSON response".encode()
        with mock.patch("requests.request", return_value=self.response):
            with self.assertRaises(DepositApiException) as cm:
                self.rest_adapter._do('GET', '')
        self.assertEqual(str(cm.exception), "Bad JSON in response")

    def test_do_request_exception(self):
        with mock.patch("requests.request", side_effect=requests.exceptions.RequestException()):
            with self.assertRaises(DepositApiException) as cm:
                self.rest_adapter._do('GET', '')
        self.assertEqual(str(cm.exception), "Failed to access the API")

    def test_get(self):
        with mock.patch.object(RestAdapter, "_do", return_value=self.deposit_response) as mock_do:
            result = self.rest_adapter.get('endpoint', {'param': 'value'})
        mock_do.assert_called_once_with(http_method='GET', endpoint='endpoint', params={'param': 'value'})
        self.assertIsInstance(result, Response)
        self.assertEqual(result.status_code, 200)

    def test_post(self):
        with mock.patch.object(RestAdapter, "_do", return_value=self.deposit_response) as mock_do:
            result = self.rest_adapter.post('endpoint', {'param': 'value'}, data={})
        mock_do.assert_called_once_with(http_method='POST', endpoint='endpoint', params={'param': 'value'}, data={})
        self.assertIsInstance(result, Response)
        self.assertEqual(result.status_code, 200)

    def test_delete(self):
        with mock.patch.object(RestAdapter, "_do", return_value=self.deposit_response) as mock_do:
            result = self.rest_adapter.delete('endpoint', {'param': 'value'}, data={})
        mock_do.assert_called_once_with(http_method='DELETE', endpoint='endpoint', params={'param': 'value'}, data={})
        self.assertIsInstance(result, Response)
        self.assertEqual(result.status_code, 200)

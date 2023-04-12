import requests
import requests.packages
import logging
from typing import Dict, Union, List
from json import JSONDecodeError
from deposit.exceptions import DepositApiException
from deposit.models import Response


class RestAdapter:
    def __init__(self, hostname: str, api_key: str = '', ver: str = 'v1', ssl_verify: bool = True,
                 logger: logging.Logger = None):
        """
        Constructor for RestAdapter
        :param hostname: Normally, api.thecatapi.com
        :param api_key: (optional) string used for authentication when POSTing or DELETEing
        :param ver: always v1
        :param ssl_verify: Normally set to True, but if having SSL/TLS cert validation issues, can turn off with False
        :param logger: (optional) If your app has a logger, pass it in here.
        """
        self._logger = logger or logging.getLogger(__name__)
        self.url = "{}/api/{}/".format(hostname, ver)
        self._api_key = api_key
        self._ssl_verify = ssl_verify
        if not ssl_verify:
            requests.packages.urllib3.disable_warnings()

    def _do(self, http_method: str, endpoint: str, params: Dict = None, data: Union[Dict, List] = None, files: Dict = None, content_type: str = "application/json") -> Response:
        """
        Private method to perform API calls
        :param http_method: GET/POST/DELETE
        :param endpoint: endpoint path
        :param params: Dictionary with requests params
        :param data: Dictionary with request data
        :param files: Files to be uploaded
        :param content_type Request content type
        :return: API Response
        """
        full_url = self.url + endpoint
        headers = {
            'Authorization': f"Bearer {self._api_key}"
        }
        if content_type:
            headers["Content-Type"] = content_type
        log_line_pre = f"method={http_method}, url={full_url}, params={params}"
        log_line_post = ', '.join((log_line_pre, "success={}, status_code={}, message={}"))
        try:
            self._logger.debug(msg=log_line_pre)
            response = requests.request(method=http_method, url=full_url, verify=self._ssl_verify, headers=headers,
                                        params=params, data=data, files=files)
        except requests.exceptions.RequestException as e:
            self._logger.error(msg=(str(e)))
            raise DepositApiException("Failed to access the API")
        try:
            data_out = response.json()
        except (ValueError, JSONDecodeError) as e:
            self._logger.error(msg=log_line_post.format(False, None, e))
            raise DepositApiException("Bad JSON in response")
        is_success = 299 >= response.status_code >= 200
        log_line = log_line_post.format(is_success, response.status_code, response.reason)
        if is_success:
            self._logger.debug(msg=log_line)
            return Response(response.status_code, response.reason, data_out)
        self._logger.error(msg=log_line)
        raise DepositApiException(f"{response.status_code}: {response.reason}")

    def get(self, endpoint: str, params: Dict = None, content_type: str = "application/json") -> Response:
        """
        Perform GET requests
        :param endpoint: endpoint path
        :param params: Dictionary with requests params
        :param content_type Request content type
        :return: API Response
        """
        return self._do(http_method='GET', endpoint=endpoint, params=params, content_type=content_type)

    def post(self, endpoint: str, params: Dict = None, data: Union[Dict, List] = None, files: Dict = None, content_type: str = "application/json") -> Response:
        """
        Perform GET requests
        :param endpoint: endpoint path
        :param params: Dictionary with requests params
        :param data: Dictionary with requests data
        :param files: Files to be uploaded
        :param content_type Request content type
        :return: API response
        """
        return self._do(http_method='POST', endpoint=endpoint, params=params, data=data, files=files, content_type=content_type)

    def delete(self, endpoint: str, params: Dict = None, data: Dict = None, content_type: str = "application/json") -> Response:
        """
        Perform DELETE requests
        :param endpoint: endpoint path
        :param params: Dictionary with requests params
        :param data: Dictionary with requests data
        :param content_type Request content type
        :return: API response
        """
        return self._do(http_method='DELETE', endpoint=endpoint, params=params, data=data, content_type=content_type)

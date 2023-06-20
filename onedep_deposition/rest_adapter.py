import requests
import requests.packages
import logging
from typing import Dict, Union, List
from json import JSONDecodeError
from onedep_deposition.exceptions import DepositApiException, InvalidDepositSiteException
from onedep_deposition.models import Response


class RestAdapter:
    def __init__(self, hostname: str, api_key: str = '', ver: str = 'v1', ssl_verify: bool = True, timeout: int = 300,
                 logger: logging.Logger = None):
        """
        Constructor for RestAdapter
        :param hostname: Normally, api.thecatapi.com
        :param api_key: (optional) string used for authentication when POSTing or DELETEing
        :param ver: always v1
        :param ssl_verify: Normally set to True, but if having SSL/TLS cert validation issues, can turn off with False
        :param timeout: (optional) Timeout in seconds for API calls
        :param logger: (optional) If your app has a logger, pass it in here.
        """
        self._logger = logger or logging.getLogger(__name__)
        self._version = ver
        self._hostname = hostname
        self.url = "{}/api/{}/".format(hostname, ver)
        self._api_key = api_key
        self._ssl_verify = ssl_verify
        self._timeout = timeout
        if not ssl_verify:
            requests.packages.urllib3.disable_warnings()  # pylint: disable=no-member

    @property
    def hostname(self) -> str:
        """
        Getter for hostname
        :return: hostname
        """
        return self._hostname

    @hostname.setter
    def hostname(self, hostname: str) -> None:
        """
        Setter for hostname
        :param hostname: hostname
        :return: None
        """
        self.url = "{}/api/{}/".format(hostname, self._version)

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
            if 'Content-Type' in headers and headers['Content-Type'] == 'application/json':
                response = requests.request(method=http_method, url=full_url, verify=self._ssl_verify, headers=headers,
                                            params=params, json=data, files=files, timeout=self._timeout)
            else:
                response = requests.request(method=http_method, url=full_url, verify=self._ssl_verify, headers=headers,
                                            params=params, data=data, files=files, timeout=self._timeout)
        except requests.exceptions.RequestException as e:
            self._logger.error(msg=(str(e)))
            raise DepositApiException("Failed to access the API", 403) from e
        if response.status_code == 204:
            # Django is redirecting 204 to OneDep home page
            return Response(204)
        is_success = 299 >= response.status_code >= 200
        log_line = log_line_post.format(is_success, response.status_code, response.reason)
        if not is_success:
            self._logger.error(msg=log_line)
            raise DepositApiException(response.reason, response.status_code)
        try:
            data_out = response.json()
        except (ValueError, JSONDecodeError) as e:
            self._logger.error(msg=log_line_post.format(False, None, e))
            raise DepositApiException("Bad JSON in response", 502) from e
        self._logger.debug(msg=log_line)

        if 'extras' in data_out and 'code' in data_out:
            if 'invalid_location' in data_out['code'] and 'base_url' in data_out['extras']:
                self._logger.warning(msg=f"Invalid deposit site, expected is {data_out['extras']['base_url']}")
                raise InvalidDepositSiteException(data_out['extras']['base_url'])
        return Response(response.status_code, response.reason, data_out)

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

import logging
from deposit.rest_adapter import RestAdapter
from deposit.exceptions import DepositApiException
from deposit.models import *


class DepositApi:
    # TODO: Change default hostname
    def __init__(self, hostname: str = 'http://local.wwpdb.org:12000/deposition', api_key: str = '', ver: str = 'v1',
                 ssl_verify: bool = True, logger: logging.Logger = None):
        self.rest_adapter = RestAdapter(hostname, api_key, ver, ssl_verify, logger)

    def get_deposition(self, dep_id: str):
        response = self.rest_adapter.get(f"depositions/{dep_id}")
        deposit = Deposit(**response.data)
        return deposit

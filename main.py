from deposit.rest_adapter import RestAdapter
from deposit.models import *
from deposit.deposit_api import DepositApi

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMDA5LTAwMDUtNzk3OS03NDY2IiwiZXhwIjoxNjgwOTY0MDI3LCJpYXQiOjE2Nzk2NjgwMjd9.T_myagpIIn7ZMNdJS0NpIgc2kY1UFp8Bu8bzHRXwHEg"
BASE_URL = "http://local.wwpdb.org:12000/deposition"
VERIFY_SSL = False


def debug_rest_adapter():
    api = DepositApi(hostname=BASE_URL, ssl_verify=False, api_key=API_KEY)
    print(api.get_deposition("D_8233000014"))


if __name__ == '__main__':
    debug_rest_adapter()

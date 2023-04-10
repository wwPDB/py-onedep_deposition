from deposit.rest_adapter import RestAdapter
from deposit.models import *
from deposit.deposit_api import DepositApi
from deposit.enum import Country, EMSubType

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMDA5LTAwMDUtNzk3OS03NDY2IiwiZXhwIjoxNjgxNDg0NDczLCJpYXQiOjE2ODAxODg0NzN9.Sq4nV16MjvXspibxLRoX4CzVlvy6fpbcKCg-0tmXtxI"
BASE_URL = "http://local.wwpdb.org:12000/deposition"
VERIFY_SSL = False

def debug_rest_adapter():
    api = DepositApi(hostname=BASE_URL, ssl_verify=False, api_key=API_KEY)
    # depositions = api.get_depositions_by_user()
    # deposition = api.get_deposition("D_8233000014")
    # print(deposition)
    users = api.get_users("D_8233000018")

    # New deposition
    # experiments = deposition.experiments
    # new_deposition = api.create_deposition("neli@ebi.ac.uk", ["0009-0005-7979-7466"], "United Kingdom", experiments)
    # new_deposition = api.create_em_deposition("neli@ebi.ac.uk", ["0009-0005-7979-7466"], Country.UK, subtype=EMSubType.SPA)
    # for deposition in depositions:
    #     print(deposition)
    print(users)

if __name__ == '__main__':
    debug_rest_adapter()

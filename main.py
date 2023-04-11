from deposit.rest_adapter import RestAdapter
from deposit.models import *
from deposit.deposit_api import DepositApi
from deposit.enum import Country, EMSubType

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMDA5LTAwMDUtNzk3OS03NDY2IiwiZXhwIjoxNjgxNDg0NDczLCJpYXQiOjE2ODAxODg0NzN9.Sq4nV16MjvXspibxLRoX4CzVlvy6fpbcKCg-0tmXtxI"
BASE_URL = "http://local.wwpdb.org:12000/deposition"
VERIFY_SSL = False

def debug_rest_adapter():
    api = DepositApi(hostname=BASE_URL, ssl_verify=False, api_key=API_KEY)
    # depositions = api.get_all_depositions()

    # users = api.add_user("D_8233000014", orcid="0000-0001-6466-8083")
    # print(users)

    deleted_user = api.remove_user("D_8233000014", orcid="0000-0001-6466-8083")

    # deposition = api.get_deposition("D_8233000014")
    # print(deposition)

    # New deposition
    # experiments = deposition.experiments
    # new_deposition = api.create_deposition("neli@ebi.ac.uk", ["0009-0005-7979-7466"], "United Kingdom", experiments)
    # new_deposition = api.create_em_deposition("neli@ebi.ac.uk", ["0009-0005-7979-7466"], Country.UK, subtype=EMSubType.SPA)
    # for deposition in depositions:
    #     print(deposition)


if __name__ == '__main__':
    debug_rest_adapter()

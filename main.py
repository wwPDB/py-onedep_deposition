from deposit.rest_adapter import RestAdapter
from deposit.models import *
from deposit.deposit_api import DepositApi
from deposit.enum import Country, EMSubType

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMDA5LTAwMDUtNzk3OS03NDY2IiwiZXhwIjoxNjgzMDMxODgzLCJpYXQiOjE2ODE3MzU4ODN9.j85nBRmBUBRvUMntnD6KEn7eNdifHIP7MBmnMkGdauY"
BASE_URL = "http://local.wwpdb.org:12000/deposition"
VERIFY_SSL = False

def debug_rest_adapter():
    api = DepositApi(hostname=BASE_URL, ssl_verify=False, api_key=API_KEY)
    # depositions = api.get_all_depositions()
    # print(depositions)

    users = api.add_user("D_8233000014", orcid="0000-0001-6466-8083")
    print(users)

    # deleted_user = api.remove_user("D_8233000014", orcid="0000-0001-6466-8083")

    # deposition = api.get_deposition("D_8233000014")
    # print(deposition)

    # New deposition
    # experiments = deposition.experiments
    # new_deposition = api.create_deposition("neli@ebi.ac.uk", ["0009-0005-7979-7466"], "United Kingdom", experiments)
    # new_deposition = api.create_em_deposition("neli@ebi.ac.uk", ["0009-0005-7979-7466"], Country.UK, subtype=EMSubType.SPA)
    # for deposition in depositions:
    #     print(deposition)

    # Files
    # file = api.upload_file("D_8233000014", "/Users/neli/Downloads/8f2i.cif", "co-pdb", overwrite=True)
    # api.remove_file("D_8233000014", 25)
    # files = api.get_files("D_8233000014")
    # print(len(files))

    # Status
    # response = api.process("D_8233000014")
    # print(response)

    # status = api.get_status("D_8233000014")
    # print(status)

if __name__ == '__main__':
    debug_rest_adapter()

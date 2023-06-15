from onedep_deposition.deposit_api import DepositApi
from onedep_deposition.enum import *

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMDA5LTAwMDUtNzk3OS03NDY2IiwiZXhwIjoxNjg3OTQ0OTczLCJpYXQiOjE2ODY2NDg5NzN9.KT_wgrsTStXJ3pGJEYVtTtsGoxuhibhOy5WTCPCxawI"
BASE_URL = "http://local.wwpdb.org:12000/deposition"
VERIFY_SSL = False


def debug_rest_adapter():
    api = DepositApi(hostname=BASE_URL, ssl_verify=False, api_key=API_KEY)

    # #Show all depositions
    # depositions = api.get_all_depositions()
    # print(f"All depositions: {depositions}")
    #
    # #Show deposition by id
    # deposition = api.get_deposition("D_8233000014")
    # print(f"Deposition: {deposition}")

    #Create new deposition
    # new_deposition = api.create_em_deposition("neli@ebi.ac.uk", ["0009-0005-7979-7466"], Country.UK, subtype=EMSubType.SPA)
    # print(f"New deposition: {new_deposition}")

    #Upload file
    # file = api.upload_file("D_8233000014", "/Users/neli/Downloads/8f2i.cif", "co-pdb", overwrite=False)
    # print(f"Uploaded file: {file}")
    #
    # #Show all files
    # files = api.get_files("D_8233000014")
    # print(f"All files: {files}")
    #
    # #Add new user
    # user = api.add_user("D_8233000014", orcid="0000-0001-6466-8083")
    # print(f"New user: {user}")
    #
    # #Delete user
    # deleted_user = api.remove_user("D_8233000014", orcid="0000-0001-6466-8083")
    # print(f"Deleted user: {deleted_user}")


if __name__ == '__main__':
    debug_rest_adapter()
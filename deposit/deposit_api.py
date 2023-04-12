import logging
from typing import Union
from deposit.rest_adapter import RestAdapter
from deposit.exceptions import DepositApiException
from deposit.models import *
from deposit.enum import Country, EMSubType, FileType
import mimetypes
import os


class DepositApi:
    # TODO: Change default hostname
    def __init__(self, hostname: str = 'http://local.wwpdb.org:12000/deposition', api_key: str = '', ver: str = 'v1',
                 ssl_verify: bool = True, logger: logging.Logger = None):
        """
        Constructor method for DepositAPI wrapper
        :param hostname: Site url
        :param api_key: User public API key
        :param ver: version (usually v1)
        :param ssl_verify: Perform a SSL verification? True for production
        :param logger: Attach a logger
        """
        self.rest_adapter = RestAdapter(hostname, api_key, ver, ssl_verify, logger)

    def create_deposition(self, email: str, users : List[str], country : Country, experiments : List[Experiment], password : str = ""):
        """
        General method to create a deposition passing an Experiment object
        :param email: User e-mail
        :param users: List of ORCID ids that can access this deposition
        :param country: Country from enum list
        :param experiments: List of Experiment objects
        :param password: Password
        :return: Response
        """
        data = {
            "email": email,
            "users": users,
            "country": country.value,
            "experiments": [experiment.json() for experiment in experiments]
        }
        if password:
            data["password"] = password
        response = self.rest_adapter.post("depositions/new", data=data)
        return response

    def create_em_deposition(self, email: str, users : List[str], country : Country, subtype: Union[EMSubType, str], related_emdb: str = None, password : str = ""):
        """
        Create an EM deposition
        :param email: User e-mail
        :param users: List of ORCID ids that can access this deposition
        :param country: Country from enum list
        :param subtype: EM sub type, accepts enum or string
        :param related_emdb: Related EMDB id
        :param password: Password
        :return: Response
        """
        experiment = Experiment(exp_type="em", subtype=subtype, related_emdb=related_emdb)
        response = self.create_deposition(email=email, users=users, country=country, experiments=[experiment], password=password)
        return response

    def create_xray_deposition(self,  email: str, users : List[str], country : Country, password : str = ""):
        """
        Create an XRAY deposition
        :param email: User e-mail
        :param users: List of ORCID ids that can access this deposition
        :param country: Country from enum list
        :param password: Password
        :return: Response
        """
        experiment = Experiment(exp_type="xray")
        response = self.create_deposition(email=email, users=users, country=country, experiments=[experiment], password=password)
        return response

    def create_fiber_deposition(self,  email: str, users : List[str], country : Country, password : str = ""):
        """
        Create a Fiber diffraction deposition
        :param email: User e-mail
        :param users: List of ORCID ids that can access this deposition
        :param country: Country from enum list
        :param password: Password
        :return: Response
        """
        experiment = Experiment(exp_type="fiber")
        response = self.create_deposition(email=email, users=users, country=country, experiments=[experiment], password=password)
        return response

    def create_neutron_deposition(self,  email: str, users : List[str], country : Country, password : str = ""):
        """
        Create a Neutron diffraction deposition
        :param email: User e-mail
        :param users: List of ORCID ids that can access this deposition
        :param country: Country from enum list
        :param password: Password
        :return: Response
        """
        experiment = Experiment(exp_type="neutron")
        response = self.create_deposition(email=email, users=users, country=country, experiments=[experiment], password=password)
        return response

    def create_ec_deposition(self,  email: str, users : List[str], country : Country, password : str = "", related_emdb: str = None):
        """
        Create an Electron crystallography deposition
        :param email: User e-mail
        :param users: List of ORCID ids that can access this deposition
        :param country: Country from enum list
        :param password: Password
        :param related_emdb: Related EMDB id
        :return: Response
        """
        experiment = Experiment(exp_type="ec", related_emdb=related_emdb)
        response = self.create_deposition(email=email, users=users, country=country, experiments=[experiment], password=password)
        return response

    def create_nmr_deposition(self,  email: str, users : List[str], country : Country, password : str = "", related_bmrb: str = None):
        """
        Create a NMR deposition
        :param email: User e-mail
        :param users: List of ORCID ids that can access this deposition
        :param country: Country from enum list
        :param password: Password
        :param related_bmrb: Related BMRB id
        :return: Response
        """
        experiment = Experiment(exp_type="nmr", related_bmrb=related_bmrb)
        response = self.create_deposition(email=email, users=users, country=country, experiments=[experiment], password=password)
        return response

    def create_ssnmr_deposition(self,  email: str, users : List[str], country : Country, password : str = "", related_bmrb: str = None):
        """
        Create a Solid-state NMR E deposition
        :param email: User e-mail
        :param users: List of ORCID ids that can access this deposition
        :param country: Country from enum list
        :param password: Password
        :param related_bmrb: Related BMRB id
        :return: Response
        """
        experiment = Experiment(exp_type="ssnmr", related_bmrb=related_bmrb)
        response = self.create_deposition(email=email, users=users, country=country, experiments=[experiment], password=password)
        return response

    def get_deposition(self, dep_id: str):
        """
        Get deposition from ID
        :param dep_id: Deposition ID
        :return: Deposit
        """
        response = self.rest_adapter.get(f"depositions/{dep_id}")
        deposit = Deposit(**response.data)
        return deposit

    def get_all_depositions(self):
        """
        Get all depositions from an user
        :return: List[Deposit]
        """
        depositions = []
        response = self.rest_adapter.get("depositions/")
        for deposition_json in response.data["items"]:
            deposition = Deposit(**deposition_json)
            depositions.append(deposition)
        return depositions

    def get_users(self, dep_id: str):
        """
        Get users from deposition
        :param dep_id:
        :return: Depositor
        """
        # TODO: This endpoint is missing
        response = self.rest_adapter.get(f"depositions/{dep_id}/users")
        # FIXME
        return None

    def add_user(self, dep_id: str, orcid: Union[List, str]):
        """
        Grant access from given users to deposition
        :param dep_id: Deposition ID
        :param orcid: Orcid ID or list of Orcid ids
        :return: List of depositors
        """
        users = []
        data = []
        if type(orcid) == str:
            data.append({'orcid': orcid})
        elif type(orcid) == list:
            for orcid_id in orcid:
                data.append({'orcid': orcid_id})
        response = self.rest_adapter.post(f"depositions/{dep_id}/users/", data=data)
        for user_json in response.data:
            users.append(Depositor(**user_json))

        return users

    def remove_user(self, dep_id: str, orcid: str):
        """
        Remove access from an user to a deposition
        :param dep_id: Deposition id
        :param orcid: Orcid id
        :return: Depositor
        """
        # TODO: This endpoint is not returning a message
        response = self.rest_adapter.delete(f"depositions/{dep_id}/users/{orcid}")
        # FIXME
        return None

    def upload_file(self, dep_id: str, file_path: str, file_type: Union[str, FileType]) -> FileResponse:
        """
        Upload a file in a deposition
        :param dep_id: Deposition id
        :param file_path: File path
        :param file_type: Deposition file type
        :return: File response
        """
        files = {}
        file_type_str = file_type

        if type(file_type) == FileType:
            file_type_str = file_type.value

        mime_type, encoding = mimetypes.guess_type(file_path)
        file_name = os.path.basename(file_path)

        data = {
            "name": file_name,
            "type": file_type_str
        }

        with open(file_path, "rb") as fp:
            files["file"] = (file_name, fp, mime_type)
            response = self.rest_adapter.post(f"depositions/{dep_id}/files/", data=data, files=files, content_type="")
            response.data["file_type"] = response.data.pop("type")

            return FileResponse(**response.data)

    # TODO: Add get user endpoint
    # TODO: Add remove user endpoint
    # TODO: Add get file endpoints
    # TODO: Add process files endpoint
    # TODO: Think and add composite endpoints




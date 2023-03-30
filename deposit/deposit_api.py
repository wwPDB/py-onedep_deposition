import logging
from typing import Union
from deposit.rest_adapter import RestAdapter
from deposit.exceptions import DepositApiException
from deposit.models import *
from deposit.enum import Country, EMSubType


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

    def get_depositions_by_user(self):
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



import logging
from deposit.rest_adapter import RestAdapter
from deposit.exceptions import DepositApiException
from deposit.models import *
from deposit.enum import Country


class DepositApi:
    # TODO: Change default hostname
    def __init__(self, hostname: str = 'http://local.wwpdb.org:12000/deposition', api_key: str = '', ver: str = 'v1',
                 ssl_verify: bool = True, logger: logging.Logger = None):
        self.rest_adapter = RestAdapter(hostname, api_key, ver, ssl_verify, logger)

    def create_deposition(self, email: str, users : List[str], country : Country, experiments : List[Experiment], password : str = ""):
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

    def create_em_deposition(self, email: str, users : List[str], country : Country, subtype: str, related_emdb: str = None, password : str = ""):
        experiment = Experiment(exp_type="em", subtype=subtype, related_emdb=related_emdb)
        response = self.create_deposition(email=email, users=users, country=country, experiments=[experiment], password=password)
        return response
    #TODO: Create specific depositions passing the experiments as a parameter

    def get_deposition(self, dep_id: str):
        response = self.rest_adapter.get(f"depositions/{dep_id}")
        deposit = Deposit(**response.data)
        return deposit

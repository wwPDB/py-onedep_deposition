from typing import List, Dict, Union
from deposit.enum import Status, ExperimentType, EMSubType
from datetime import datetime


class Response:
    def __init__(self, status_code: int, message: str = '', data: List[Dict] = None):
        """
        Constructor for Response
        :param status_code: Response status code
        :param message: Message
        :param data: Response data
        """
        self.status_code = int(status_code)
        self.message = str(message)
        self.data = data if data else []

    def __str__(self):
        """
        Override string parser
        :return: String text
        """
        return f"STATUS: {self.status_code}, MESSAGE: {self.message}\n{self.data}"


class Experiment:
    def __init__(self, exp_type: Union[ExperimentType, str], subtype: Union[EMSubType, str] = None, related_emdb: str = None, related_bmrb: str = None):
        """
        Constructor for Experiment
        :param type:
        :param subtype:
        :param related_emdb:
        :param related_bmrb:
        """
        self.type = None
        self.subtype = None
        self.related_emdb = str(related_emdb)
        self.related_bmrb = str(related_bmrb)

        if type(exp_type) == ExperimentType:
            self.type = exp_type
        elif exp_type:
            self.type = ExperimentType(exp_type)
        if type(subtype) == EMSubType:
            self.subtype = subtype
        elif subtype:
            self.subtype = EMSubType(subtype)

    def json(self):
        json_object = self.__dict__.copy()
        if self.type:
            json_object['type'] = self.type.value
        if self.subtype:
            json_object['subtype'] = self.subtype.value
        return json_object

class DepositError:
    def __init__(self, code: str, message: str, extras):
        """
        Constructor for DepositError
        :param code:
        :param message:
        :param extras:
        """
        self.code = str(code)
        self.message = str(message)
        self.extras = extras

    def json(self):
        return self.__dict__.copy()

class Deposit:
    def __init__(self, email: str, id: str, entry_id: str, title: str, created: str, last_login: str, site: str, status: Status, experiments: List = None, errors: List = None):
        """
        Constructor for Deposit
        :param email:
        :param dep_id:
        :param entry_id:
        :param title:
        :param created:
        :param last_login:
        :param site:
        :param status:
        :param experiments:
        :param errors:
        """
        self.email = str(email)
        self.dep_id = str(id)
        self.entry_id = str(entry_id)
        self.title = str(title)
        self.created = datetime.fromisoformat(created)
        self.last_login = datetime.fromisoformat(last_login)
        self.site = str(site)
        self.status = getattr(Status, status)
        self.experiments = []
        self.errors = []

        if experiments:
            for exp in experiments:
                #Replace reserved work type
                if "type" in exp:
                    exp["exp_type"] = exp.pop("type")
                self.experiments.append(Experiment(**exp))
        if errors:
            for error in errors:
                self.errors.append(DepositError(**error))

    def __str__(self):
        return f"ID: {self.dep_id}\nE-mail: {self.email}\nEntry ID: {self.entry_id}\nTitle: {self.title}\nCreated: {self.created}\nLast login: {self.last_login}\nSite: {self.site}\nStatus: {self.status}\nExperiments: {self.experiments}\nErrors: {self.errors}"

    def json(self):
        json_object = self.__dict__.copy()
        json_object['experiments'] = []
        json_object['errors'] = []
        json_object['status'] = self.status.name
        for experiment in self.experiments:
            json_object['experiments'].append(experiment.json())
        for error in self.errors:
            json_object['errors'].append(error.json())

        return json_object

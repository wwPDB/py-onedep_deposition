from typing import List, Dict, Union
from onedep_deposition.enum import Status, ExperimentType, EMSubType, FileType
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
    def __init__(self, exp_type: Union[ExperimentType, str], subtype: Union[EMSubType, str] = None,
                 related_emdb: str = None, related_bmrb: str = None):
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

    def __str__(self):
        message = f"TYPE: {self.type}"
        if self.subtype:
            message += f" ({self.subtype})"
        if self.related_emdb:
            message += f" [{self.related_emdb}]"
        elif self.related_bmrb:
            message += f" [{self.related_bmrb}]"
        return message

    def json(self):
        json_object = self.__dict__.copy()
        if self.type:
            json_object['type'] = self.type.value
        if self.subtype:
            json_object['subtype'] = self.subtype.value
        return json_object


class DepositError:
    def __init__(self, code: str, message: str, extras: str = None):
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
    def __init__(self, email: str, id: str, entry_id: str, title: str, created: str, last_login: str, site: str,
                 status: Status, experiments: List = None, errors: List = None, site_url: str = None):
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
        :param site_url
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
        self.site_url = str(site_url)

        if experiments:
            for exp in experiments:
                # Replace reserved work type
                if "type" in exp:
                    exp["exp_type"] = exp.pop("type")
                self.experiments.append(Experiment(**exp))
        # FIXME: Error ta vindo so como string
        if errors:
            for error in errors:
                self.errors.append(DepositError(**error))

    def __str__(self):
        return f"ID: {self.dep_id}\nE-mail: {self.email}\nEntry ID: {self.entry_id}\nTitle: {self.title}\nCreated: {self.created}\nLast login: {self.last_login}\nSite: {self.site}\nStatus: {self.status}\nSite URL: {self.site_url}\nExperiments: {self.experiments}\nErrors: {self.errors}"

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


class Depositor:
    def __init__(self, orcid: str, id: int, full_name: str, last_login: str = None, date_joined: str = None,
                 depositions: List[Deposit] = None):
        self.orcid = str(orcid)
        self.id = int(id)
        self.full_name = str(full_name),
        self.last_login = datetime.fromisoformat(last_login) if last_login else None
        self.date_joined = datetime.fromisoformat(date_joined) if date_joined else None
        self.depositions = []

        if depositions:
            for deposition in depositions:
                depositions.append(**deposition)

    def __str__(self):
        return f"Name: {self.full_name} [{self.id}]\nORCID: {self.orcid}\nDate joined: {self.date_joined}\nLast login: {self.last_login}\nDepositions: {self.depositions}"

    def json(self):
        json_object = self.__dict__.copy()
        json_object["depositions"] = []

        for deposition in self.depositions:
            json_object["depositions"].append(deposition.json())

        return json_object


class DepositedFile:
    def __init__(self, id: int, created: str, name: str, file_type: Union[str, FileType], errors: List[str] = None,
                 warnings: List[str] = None):
        self.id = int(id)
        self.name = str(name)

        date_format = "%A, %B %d, %Y %H:%M:%S"
        self.created = datetime.strptime(created, date_format)

        if type(file_type) == str:
            self.type = FileType(file_type)
        else:
            self.type = file_type

        self.errors = [error for error in errors if error != ""] if errors else []
        self.warnings = [warning for warning in warnings if warning != ""] if warnings else []

    def __str__(self):
        message = f"ID: {self.id}\nCREATED ON: {self.created}\nNAME: {self.name}\nTYPE: {self.type}\nERRORS:\n"
        for error in self.errors:
            message += f"  -{error}\n"
        message += f"\nWARNINGS:\n"
        for warning in self.warnings:
            message += f"  -{warning}\n"

        return message


class DepositedFilesSet:
    def __init__(self, files: List[Dict], errors: List[str] = None, warnings: List[str] = None):
        self.files = []
        self.errors = [error for error in errors if error != ""] if errors else []
        self.warnings = [warning for warning in warnings if warning != ""] if errors else []

        for file in files:
            file["file_type"] = file.pop("type")
            self.files.append(DepositedFile(**file))

    def __getitem__(self, index):
        return self.files[index]

    def __len__(self):
        return len(self.files)

    def __iter__(self):
        self.current_index = 0
        return self

    def __next__(self):
        if self.current_index < len(self.files):
            item = self.files[self.current_index]
            self.current_index += 1
            return item
        raise StopIteration

class DepositStatus:
    def __init__(self, status: str, action: str, step: str, details: str, date: str):
        self.status = str(status)
        self.action = str(action)
        self.step = str(step)
        self.details = str(details)
        self.date = datetime.fromisoformat(date)

    def __str__(self):
        return f"STATUS: {self.status}\nSTEP: {self.step}\nDATE: {self.date}\nACTION: {self.action}\nDETAILS: {self.details}"

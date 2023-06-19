from typing import List, Dict, Union
from onedep_deposition.enum import Status, ExperimentType, EMSubType, FileType
from datetime import datetime


class Response:
    """Class representing an API response"""
    def __init__(self, status_code: int, message: str = '', data: List[Dict] = None):
        """
        Constructor for Response
        :param status_code: Response status code
        :param message: Message
        :param data: Response data
        """
        self._status_code = int(status_code)
        self._message = str(message)
        self._data = data if data else []

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def message(self) -> str:
        return self._message

    @property
    def data(self) -> List[Dict]:
        return self._data

    def __str__(self):
        """
        Override string parser
        :return: String text
        """
        return f"STATUS: {self._status_code}, MESSAGE: {self._message}\n{self._data}"


class Experiment:
    """Class representing an experiment"""
    def __init__(self, exp_type: Union[ExperimentType, str], subtype: Union[EMSubType, str] = None,
                 related_emdb: str = None, related_bmrb: str = None):
        """
        Constructor for Experiment
        :param type:
        :param subtype:
        :param related_emdb:
        :param related_bmrb:
        """
        self._type = None
        self._subtype = None
        self._related_emdb = str(related_emdb) if related_emdb is not None else None
        self._related_bmrb = str(related_bmrb) if related_bmrb is not None else None

        if type(exp_type) == ExperimentType:
            self._type = exp_type
        elif exp_type:
            self._type = ExperimentType(exp_type)
        if type(subtype) == EMSubType:
            self._subtype = subtype
        elif subtype:
            self._subtype = EMSubType(subtype)

    @property
    def type(self) -> Union[ExperimentType, None]:
        return self._type

    @property
    def subtype(self) -> Union[EMSubType, None]:
        return self._subtype

    @property
    def related_emdb(self) -> str:
        return self._related_emdb

    @property
    def related_bmrb(self) -> str:
        return self._related_bmrb

    def __str__(self):
        message = f"TYPE: {self._type}"
        if self.subtype:
            message += f" ({self._subtype})"
        if self.related_emdb:
            message += f" [{self._related_emdb}]"
        elif self.related_bmrb:
            message += f" [{self._related_bmrb}]"
        return message

    def json(self):
        json_object = self.__dict__.copy()
        json_object = {key[1:]: value for key, value in json_object.items() if value is not None}

        if self.type:
            json_object['type'] = self._type.value
        if self.subtype:
            json_object['subtype'] = self._subtype.value
        return json_object


class DepositError:
    """Class representing an deposit error"""
    def __init__(self, code: str, message: str, extras: str = None):
        """
        Constructor for DepositError
        :param code:
        :param message:
        :param extras:
        """
        self._code = str(code)
        self._message = str(message)
        self._extras = extras

    @property
    def code(self) -> str:
        return self._code

    @property
    def message(self) -> str:
        return self._message

    @property
    def extras(self) -> str:
        return self._extras

    def json(self):
        json_object = self.__dict__.copy()
        json_object = {key[1:]: value for key, value in json_object.items() if value is not None}
        return json_object

    def __str__(self):
        return f"CODE: {self._code}, MESSAGE: {self._message}\nEXTRAS: {self._extras}"


class Deposit:
    """Class representing an deposit"""
    # TODO: Replace id for dep_id
    def __init__(self, email: str, id: str, entry_id: str, title: str, created: str, last_login: str, site: str,  # pylint: disable=redefined-builtin
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
        self._email = str(email)
        self._id = str(id)
        self._entry_id = str(entry_id)
        self._title = str(title)
        self._created = datetime.fromisoformat(created)
        self._last_login = datetime.fromisoformat(last_login)
        self._site = str(site)
        self._status = getattr(Status, status)
        self._experiments = []
        self._errors = []
        self._site_url = str(site_url) if site_url is not None else None

        if experiments:
            for exp in experiments:
                # Replace reserved work type
                if "type" in exp:
                    exp["exp_type"] = exp.pop("type")
                self._experiments.append(Experiment(**exp))

        if errors:
            for error in errors:
                self._errors.append(DepositError(**error))

    @property
    def email(self) -> str:
        return self._email

    @property
    def dep_id(self) -> str:
        return self._id

    @property
    def entry_id(self) -> str:
        return self._entry_id

    @property
    def title(self) -> str:
        return self._title

    @property
    def created(self) -> datetime:
        return self._created

    @property
    def last_login(self) -> datetime:
        return self._last_login

    @property
    def site(self) -> str:
        return self._site

    @property
    def status(self) -> Status:
        return self._status

    @property
    def experiments(self) -> List[Experiment]:
        return self._experiments

    @property
    def errors(self) -> List[DepositError]:
        return self._errors

    @property
    def site_url(self) -> str:
        return self._site_url

    def __str__(self):
        experiments_text = [str(exp) for exp in self._experiments]
        return f"ID: {self._id}\nE-mail: {self._email}\nEntry ID: {self._entry_id}\nTitle: {self._title}\nCreated: {self._created}\nLast login: {self._last_login}\nSite: {self._site}\nStatus: {self._status}\nSite URL: {self._site_url}\nExperiments: {experiments_text}\nErrors: {self._errors}"  # noqa: E501

    def json(self):
        json_object = self.__dict__.copy()
        json_object = {key[1:]: value for key, value in json_object.items() if value is not None}
        json_object['experiments'] = []
        json_object['errors'] = []
        json_object['status'] = self._status.name
        for experiment in self._experiments:
            json_object['experiments'].append(experiment.json())
        for error in self._errors:
            json_object['errors'].append(error.json())

        return json_object


class Depositor:
    """Class representing a depositor"""
    # TODO: Replace id for dep_id
    def __init__(self, orcid: str, id: int, full_name: str, last_login: str = None, date_joined: str = None,  # pylint: disable=redefined-builtin
                 depositions: List[Deposit] = None):
        """Constructor for depositor
        :param orcid:
        :param id:
        :param full_name:
        :param last_login:
        :param date_joined:
        :param depositions:
        """
        self._orcid = str(orcid)
        self._id = int(id)
        self._full_name = str(full_name)
        self._last_login = datetime.fromisoformat(last_login) if last_login else None
        self._date_joined = datetime.fromisoformat(date_joined) if date_joined else None
        self._depositions = []

        if depositions:
            for deposition in depositions:
                self._depositions.append(**deposition)

    @property
    def orcid(self) -> str:
        return self._orcid

    @property
    def id(self) -> int:
        return self._id

    @property
    def full_name(self) -> str:
        return self._full_name

    @property
    def last_login(self) -> datetime:
        return self._last_login

    @property
    def date_joined(self) -> datetime:
        return self._date_joined

    @property
    def depositions(self) -> List[Deposit]:
        return self._depositions

    def __str__(self):
        return f"Name: {self._full_name} [{self._id}]\nORCID: {self._orcid}\nDate joined: {self._date_joined}\nLast login: {self._last_login}\nDepositions: {self._depositions}"

    def json(self):
        json_object = self.__dict__.copy()
        json_object = {key[1:]: value for key, value in json_object.items() if value is not None}
        json_object["depositions"] = []

        for deposition in self._depositions:
            json_object["depositions"].append(deposition.json())

        return json_object


class DepositedFile:
    """Class representing a deposited file"""
    # TODO: Replace id for dep_id
    def __init__(self, id: int, created: str, name: str, file_type: Union[str, FileType], errors: List[str] = None,  # pylint: disable=redefined-builtin
                 warnings: List[str] = None):
        """Constructor for deposited file
        :param id:
        :param created:
        :param name:
        :param file_type:
        :param errors:
        :param warnings:
        """
        self._id = int(id)
        self._name = str(name)

        date_format = "%A, %B %d, %Y %H:%M:%S"
        self._created = datetime.strptime(created, date_format)

        if isinstance(file_type, str):
            self._type = FileType(file_type)
        else:
            self._type = file_type

        self._errors = [DepositError(**error) for error in errors if error != ""] if errors else []
        self._warnings = [DepositError(**warning) for warning in warnings if warning != ""] if warnings else []

    def __str__(self):
        message = f"ID: {self._id}\nCREATED ON: {self._created}\nNAME: {self._name}\nTYPE: {self._type}\nERRORS:\n"
        for error in self._errors:
            message += f"  -{error}\n"
        message += "\nWARNINGS:\n"
        for warning in self._warnings:
            message += f"  -{warning}\n"

        return message

    @property
    def id(self) -> int:
        return self._id

    @property
    def created(self) -> datetime:
        return self._created

    @property
    def name(self) -> str:
        return self._name

    @property
    def file_type(self) -> FileType:
        return self._type

    @property
    def errors(self) -> List[str]:
        return self._errors

    @property
    def warnings(self) -> List[str]:
        return self._warnings


class DepositedFilesSet:
    """
    Class representing a set of deposited files
    """
    def __init__(self, files: List[Dict], errors: List[str] = None, warnings: List[str] = None):
        """Constructor for deposited files set"""
        self._files = []
        self._errors = [DepositError(**error) for error in errors if error != ""] if errors else []
        self._warnings = [DepositError(**warning) for warning in warnings if warning != ""] if errors else []

        self.__current_index = 0

        for file in files:
            file["file_type"] = file.pop("type")
            self._files.append(DepositedFile(**file))

    def __getitem__(self, index):
        return self._files[index]

    def __len__(self):
        return len(self._files)

    def __iter__(self):
        self.__current_index = 0
        return self

    def __next__(self):
        if self.__current_index < len(self._files):
            item = self._files[self.__current_index]
            self.__current_index += 1
            return item
        raise StopIteration

    @property
    def files(self) -> List[DepositedFile]:
        return self._files

    @property
    def errors(self) -> List[str]:
        return self._errors

    @property
    def warnings(self) -> List[str]:
        return self._warnings


class DepositStatus:
    def __init__(self, status: str, action: str, step: str, details: str, date: str):
        self._status = str(status)
        self._action = str(action)
        self._step = str(step)
        self._details = str(details)
        self._date = datetime.fromisoformat(date)

    def __str__(self):
        return f"STATUS: {self._status}\nSTEP: {self._step}\nDATE: {self._date}\nACTION: {self._action}\nDETAILS: {self._details}"

    @property
    def status(self) -> str:
        return self._status

    @property
    def action(self) -> str:
        return self._action

    @property
    def step(self) -> str:
        return self._step

    @property
    def details(self) -> str:
        return self._details

    @property
    def date(self) -> datetime:
        return self._date


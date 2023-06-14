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

    @status_code.setter
    def status_code(self, value: int):
        self._status_code = int(value)

    @property
    def message(self) -> str:
        return self._message

    @message.setter
    def message(self, value: str):
        self._message = str(value)

    @property
    def data(self) -> List[Dict]:
        return self._data

    @data.setter
    def data(self, value: List[Dict]):
        self._data = value if value else []

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
            self.type = exp_type
        elif exp_type:
            self.type = ExperimentType(exp_type)
        if type(subtype) == EMSubType:
            self.subtype = subtype
        elif subtype:
            self.subtype = EMSubType(subtype)

    @property
    def type(self) -> Union[ExperimentType, None]:
        return self._type

    @type.setter
    def type(self, value: Union[ExperimentType, None]):
        self._type = value

    @property
    def subtype(self) -> Union[EMSubType, None]:
        return self._subtype

    @subtype.setter
    def subtype(self, value: Union[EMSubType, None]):
        self._subtype = value

    @property
    def related_emdb(self) -> str:
        return self._related_emdb

    @related_emdb.setter
    def related_emdb(self, value: str):
        self._related_emdb = str(value)

    @property
    def related_bmrb(self) -> str:
        return self._related_bmrb

    @related_bmrb.setter
    def related_bmrb(self, value: str):
        self._related_bmrb = str(value)

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

    @code.setter
    def code(self, value: str):
        self._code = str(value)

    @property
    def message(self) -> str:
        return self._message

    @message.setter
    def message(self, value: str):
        self._message = str(value)

    @property
    def extras(self) -> str:
        return self._extras

    @extras.setter
    def extras(self, value: str):
        self._extras = value

    def json(self):
        json_object =  self.__dict__.copy()
        json_object = {key[1:]: value for key, value in json_object.items() if value is not None}
        return json_object


class Deposit:
    """Class representing an deposit"""
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

        # FIXME: Error is coming as a string
        if errors:
            for error in errors:
                self._errors.append(DepositError(**error))

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        self._email = str(value)

    @property
    def dep_id(self) -> str:
        return self._id

    @dep_id.setter
    def dep_id(self, value: str):
        self._id = str(value)

    @property
    def entry_id(self) -> str:
        return self._entry_id

    @entry_id.setter
    def entry_id(self, value: str):
        self._entry_id = str(value)

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        self._title = str(value)

    @property
    def created(self) -> datetime:
        return self._created

    @created.setter
    def created(self, value: str):
        self._created = datetime.fromisoformat(value)

    @property
    def last_login(self) -> datetime:
        return self._last_login

    @last_login.setter
    def last_login(self, value: str):
        self._last_login = datetime.fromisoformat(value)

    @property
    def site(self) -> str:
        return self._site

    @site.setter
    def site(self, value: str):
        self._site = str(value)

    @property
    def status(self) -> Status:
        return self._status

    @status.setter
    def status(self, value: Status):
        self._status = value

    @property
    def experiments(self) -> List[Experiment]:
        return self._experiments

    @experiments.setter
    def experiments(self, value: List[Experiment]):
        self._experiments = value if value else []

    @property
    def errors(self) -> List[DepositError]:
        return self._errors

    @errors.setter
    def errors(self, value: List[DepositError]):
        self._errors = value if value else []

    @property
    def site_url(self) -> str:
        return self._site_url

    @site_url.setter
    def site_url(self, value: str):
        self._site_url = str(value)

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
    def __init__(self, orcid: str, id: int, full_name: str, last_login: str = None, date_joined: str = None,
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

    @orcid.setter
    def orcid(self, value: str):
        self._orcid = str(value)

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = int(value)

    @property
    def full_name(self) -> str:
        return self._full_name

    @full_name.setter
    def full_name(self, value: str):
        self._full_name = str(value)

    @property
    def last_login(self) -> datetime:
        return self._last_login

    @last_login.setter
    def last_login(self, value: str):
        self._last_login = datetime.fromisoformat(value) if value else None

    @property
    def date_joined(self) -> datetime:
        return self._date_joined

    @date_joined.setter
    def date_joined(self, value: str):
        self._date_joined = datetime.fromisoformat(value) if value else None

    @property
    def depositions(self) -> List[Deposit]:
        return self._depositions

    @depositions.setter
    def depositions(self, value: List[Deposit]):
        self._depositions = value if value else []

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
    def __init__(self, id: int, created: str, name: str, file_type: Union[str, FileType], errors: List[str] = None,
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

        self._errors = [error for error in errors if error != ""] if errors else []
        self._warnings = [warning for warning in warnings if warning != ""] if warnings else []

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

    @id.setter
    def id(self, value: int):
        self._id = int(value)

    @property
    def created(self) -> datetime:
        return self._created

    @created.setter
    def created(self, value: str):
        date_format = "%A, %B %d, %Y %H:%M:%S"
        self._created = datetime.strptime(value, date_format)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = str(value)

    @property
    def file_type(self) -> FileType:
        return self._type

    @file_type.setter
    def file_type(self, value: Union[str, FileType]):
        if isinstance(value, str):
            self._type = FileType(value)
        else:
            self._type = value

    @property
    def errors(self) -> List[str]:
        return self._errors

    @errors.setter
    def errors(self, value: List[str]):
        self._errors = [error for error in value if error != ""] if value else []

    @property
    def warnings(self) -> List[str]:
        return self._warnings

    @warnings.setter
    def warnings(self, value: List[str]):
        self._warnings = [warning for warning in value if warning != ""] if value else []


class DepositedFilesSet:
    """
    Class representing a set of deposited files
    """
    def __init__(self, files: List[Dict], errors: List[str] = None, warnings: List[str] = None):
        """Constructor for deposited files set"""
        self._files = []
        self._errors = [error for error in errors if error != ""] if errors else []
        self._warnings = [warning for warning in warnings if warning != ""] if errors else []

        for file in files:
            file["file_type"] = file.pop("type")
            self._files.append(DepositedFile(**file))

    def __getitem__(self, index):
        return self._files[index]

    def __len__(self):
        return len(self._files)

    def __iter__(self):
        self._current_index = 0
        return self

    def __next__(self):
        if self._current_index < len(self._files):
            item = self._files[self._current_index]
            self._current_index += 1
            return item
        raise StopIteration

    @property
    def files(self) -> List[DepositedFile]:
        return self._files

    @files.setter
    def files(self, value: List[DepositedFile]):
        self._files = value if value else []

    @property
    def errors(self) -> List[str]:
        return self._errors

    @errors.setter
    def errors(self, value: List[str]):
        self._errors = [error for error in value if error != ""] if value else []

    @property
    def warnings(self) -> List[str]:
        return self._warnings

    @warnings.setter
    def warnings(self, value: List[str]):
        self._warnings = [warning for warning in value if warning != ""] if value else []


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

    @status.setter
    def status(self, value: str):
        self._status = str(value)

    @property
    def action(self) -> str:
        return self._action

    @action.setter
    def action(self, value: str):
        self._action = str(value)

    @property
    def step(self) -> str:
        return self._step

    @step.setter
    def step(self, value: str):
        self._step = str(value)

    @property
    def details(self) -> str:
        return self._details

    @details.setter
    def details(self, value: str):
        self._details = str(value)

    @property
    def date(self) -> datetime:
        return self._date

    @date.setter
    def date(self, value: str):
        self._date = datetime.fromisoformat(value)

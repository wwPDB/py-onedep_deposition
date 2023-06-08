import logging
from onedep_deposition.rest_adapter import RestAdapter
from onedep_deposition.models import DepositStatus, Experiment, Deposit, Depositor, DepositedFile, DepositedFilesSet
from onedep_deposition.enum import Country, EMSubType, FileType
from onedep_deposition.exceptions import DepositApiException
from typing import List, Union
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

    def create_deposition(self, email: str, users: List[str], country: Country, experiments: List[Experiment], password: str = "", **kwargs) -> Deposit:
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
        deposit = Deposit(**response.data)
        return deposit

    def create_em_deposition(self, email: str, users: List[str], country: Country, subtype: Union[EMSubType, str], related_emdb: str = None, password: str = "", **kwargs) -> Deposit:
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
        deposit = self.create_deposition(email=email, users=users, country=country, experiments=[experiment], password=password)
        return deposit

    def create_xray_deposition(self, email: str, users: List[str], country: Country, password: str = "", **kwargs) -> Deposit:
        """
        Create an XRAY deposition
        :param email: User e-mail
        :param users: List of ORCID ids that can access this deposition
        :param country: Country from enum list
        :param password: Password
        :return: Response
        """
        experiment = Experiment(exp_type="xray")
        deposit = self.create_deposition(email=email, users=users, country=country, experiments=[experiment], password=password)
        return deposit

    def create_fiber_deposition(self, email: str, users: List[str], country: Country, password: str = "", **kwargs) -> Deposit:
        """
        Create a Fiber diffraction deposition
        :param email: User e-mail
        :param users: List of ORCID ids that can access this deposition
        :param country: Country from enum list
        :param password: Password
        :return: Response
        """
        experiment = Experiment(exp_type="fiber")
        deposit = self.create_deposition(email=email, users=users, country=country, experiments=[experiment], password=password)
        return deposit

    def create_neutron_deposition(self, email: str, users: List[str], country: Country, password: str = "", **kwargs) -> Deposit:
        """
        Create a Neutron diffraction deposition
        :param email: User e-mail
        :param users: List of ORCID ids that can access this deposition
        :param country: Country from enum list
        :param password: Password
        :return: Response
        """
        experiment = Experiment(exp_type="neutron")
        deposit = self.create_deposition(email=email, users=users, country=country, experiments=[experiment], password=password)
        return deposit

    def create_ec_deposition(self, email: str, users: List[str], country: Country, password: str = "", related_emdb: str = None, **kwargs) -> Deposit:
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
        deposit = self.create_deposition(email=email, users=users, country=country, experiments=[experiment], password=password)
        return deposit

    def create_nmr_deposition(self, email: str, users: List[str], country: Country, password: str = "", related_bmrb: str = None, **kwargs) -> Deposit:
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
        deposit = self.create_deposition(email=email, users=users, country=country, experiments=[experiment], password=password)
        return deposit

    def create_ssnmr_deposition(self, email: str, users: List[str], country: Country, password: str = "", related_bmrb: str = None, **kwargs) -> Deposit:
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
        deposit = self.create_deposition(email=email, users=users, country=country, experiments=[experiment], password=password)
        return deposit

    def get_deposition(self, dep_id: str) -> Union[Deposit, None]:
        """
        Get deposition from ID
        :param dep_id: Deposition ID
        :return: Deposit
        """
        try:
            response = self.rest_adapter.get(f"depositions/{dep_id}")
            deposit = Deposit(**response.data)
        except DepositApiException as e:
            if e.status_code == 404:
                return None
            else:
                raise

        return deposit

    def get_all_depositions(self) -> List[Deposit]:
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
        response = self.rest_adapter.get(f"depositions/{dep_id}/users")  # noqa: F841
        # FIXME
        return None

    def add_user(self, dep_id: str, orcid: Union[List, str]) -> List[Depositor]:
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
        self.rest_adapter.delete(f"depositions/{dep_id}/users/{orcid}")
        return True

    def upload_file(self, dep_id: str, file_path: str, file_type: Union[str, FileType], overwrite: bool = False) -> DepositedFile:
        """
        Upload a file in a deposition
        :param dep_id: Deposition id
        :param file_path: File path
        :param file_type: Deposition file type
        :param overwrite: If true, overwrite all previously uploaded file with the same type
        :return: File response
        """
        files = {}
        file_type_str = file_type

        if not os.path.exists(file_path):
            raise DepositApiException("Invalid input file", 404)

        if type(file_type) == FileType:
            file_type_str = file_type.value

        mime_type, encoding = mimetypes.guess_type(file_path)
        file_name = os.path.basename(file_path)

        data = {
            "name": file_name,
            "type": file_type_str
        }

        if overwrite:
            deposited_files = self.get_files(dep_id)
            for file in deposited_files:
                if file.type.value == file_type_str:
                    self.remove_file(dep_id, file.id)

        with open(file_path, "rb") as fp:
            files["file"] = (file_name, fp, mime_type)
            response = self.rest_adapter.post(f"depositions/{dep_id}/files/", data=data, files=files, content_type="")
            response.data["file_type"] = response.data.pop("type")

            return DepositedFile(**response.data)

    def get_files(self, dep_id: str) -> DepositedFilesSet:
        """
        Get all files in deposition
        :param dep_id: Deposition ID
        :return: List of uploaded files
        """
        response = self.rest_adapter.get(f"depositions/{dep_id}/files/")
        return DepositedFilesSet(**response.data)

    def remove_file(self, dep_id: str, file_id: int):
        """
        Remove a file from a deposition
        :param dep_id: Deposition ID
        :param file_id: File ID
        :return: None
        """
        self.rest_adapter.delete(f"depositions/{dep_id}/files/{file_id}")
        return True

    def get_status(self, dep_id: str) -> DepositStatus:
        """
        Return the deposition status
        :param dep_id: Deposition ID
        :return: Status
        """
        response = self.rest_adapter.get(f"depositions/{dep_id}/status")
        status = DepositStatus(**response.data)
        return status

    def process(self, dep_id: str, voxel: List = None, copy_from_id: int = None, copy_contact: bool = False,
                copy_authors: bool = False, copy_citation: bool = False, copy_grant: bool = False,
                copy_em_exp_data: bool = False):
        """
        Trigger file processing
        :param dep_id: Deposition ID
        :param voxel: EM Voxel list
        :param copy_from_id: Copy metadata from another deposition?
        :param copy_contact: Copy contract metadata?
        :param copy_authors: Copy authors?
        :param copy_citation: Copy citation?
        :param copy_grant: Copy grant?
        :param copy_em_exp_data: Copy EM experimental data?
        :return: Status
        """
        copy_elements = []
        data = {}

        if copy_from_id:
            copy_elements.append("contact") if copy_contact else None
            copy_elements.append("authors") if copy_authors else None
            copy_elements.append("citation") if copy_citation else None
            copy_elements.append("grant") if copy_grant else None
            copy_elements.append("em_exp") if copy_em_exp_data else None
            data["related"] = {
                'id': copy_from_id,
                'items': copy_elements
            }

        if voxel:
            data['parameters']['voxel'] = voxel

        response = self.rest_adapter.post(f"depositions/{dep_id}/process", data=data)
        status = DepositStatus(**response.data)

        return status

    # TODO: Add get user endpoint

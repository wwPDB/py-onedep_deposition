import unittest
import tempfile
import logging
import os
from onedep_deposition.deposit_api import DepositApi
from onedep_deposition.models import Experiment, Deposit, Depositor, DepositedFile, DepositedFilesSet, DepositStatus
from onedep_deposition.enum import Country, EMSubType, FileType
from onedep_deposition.exceptions import DepositApiException
from unittest.mock import Mock


class MyDepositApi(DepositApi):
    """Wrapper class to provide access to internal rest_adapter"""
    def __init__(self, hostname: str = None, api_key: str = '', ver: str = 'v1',
                 ssl_verify: bool = True, logger: logging.Logger = None):

        super(MyDepositApi, self).__init__(hostname, api_key, ver, ssl_verify,
                                           logger)

        self.rest_adapter = self._rest_adapter


class DepositApiTests(unittest.TestCase):

    def setUp(self):
        self.deposit_api = MyDepositApi()
        self.dep_id = "D_8233000014"
        self.email = "test@ebi.ac.uk"
        self.xray = [Experiment("xray")]
        self.orcids = ["0009-0005-7979-7466", "0000-0001-6466-8083"]
        self.deposition_mocked_data = {
            "id": self.dep_id,
            "email": self.email,
            "entry_id": "?",
            "title": "?",
            "created": "2023-03-23T14:19:43.850522",
            "last_login": "2023-03-23T14:19:43.850349",
            "site": "PDBe",
            "status": "DEP",
            "site_url": "https://wwwdev.ebi.ac.uk/pdbe-da/deposition",
            "experiments": [{'type': 'xray'}],
            "errors": []
        }
        self.create_deposition_params = {
            'email': self.email,
            'users': self.orcids[:1],
            'country': Country.UK,
            'password': "password",
            'subtype': EMSubType.SPA,
            'related_emdb': "EMD-1234",
            'related_bmrb': "51899"
        }
        self.create_deposition_methods = {
            'xray': self.deposit_api.create_xray_deposition,
            'fiber': self.deposit_api.create_fiber_deposition,
            'neutron': self.deposit_api.create_neutron_deposition,
            'em': self.deposit_api.create_em_deposition,
            'ec': self.deposit_api.create_ec_deposition,
            'nmr': self.deposit_api.create_nmr_deposition,
            'ssnmr': self.deposit_api.create_ssnmr_deposition
        }
        self.user = {
            'id': 1,
            'orcid': self.orcids[0],
            'full_name': 'Name'
        }

    def test_create_generic_deposition_success(self):
        # Test a successful deposition creation
        self.deposition_mocked_data["experiments"] = [{'type': 'xray'}]
        self.create_deposition_params["experiments"] = self.xray
        self.deposit_api.rest_adapter.post = Mock(return_value=Mock(status_code=200, data=self.deposition_mocked_data))
        deposit = self.deposit_api.create_deposition(**self.create_deposition_params)
        self.assertIsInstance(deposit, Deposit, "Deposition was not created successfully")
        self.assertEqual(deposit.dep_id, self.dep_id, "Deposit ID is not correct")

    def test_create_generic_deposition_failure(self):
        # Test a failed deposition creation
        self.create_deposition_params["experiments"] = self.xray
        self.deposit_api.rest_adapter.post = Mock(side_effect=DepositApiException("Failed to create deposition", 404))
        with self.assertRaises(DepositApiException) as context:
            self.deposit_api.create_deposition(**self.create_deposition_params)
        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(str(context.exception), "Failed to create deposition", "Exception message is not correct")

    def test_create_each_method_deposition_success(self):
        # Test successful deposition creation for each method
        for method, call in self.create_deposition_methods.items():
            self.deposition_mocked_data["experiments"] = [{'type': method}]
            self.deposit_api.create_deposition = Mock(return_value=Deposit(**self.deposition_mocked_data))
            deposit = call(**self.create_deposition_params)
            self.assertIsInstance(deposit, Deposit, f"{method} deposition was not created successfully")
            self.assertEqual(deposit.dep_id, self.dep_id, "Deposit ID is not correct")

    def test_create_each_method_deposition_failure(self):
        # Test a failed EM deposition creation
        for _method, call in self.create_deposition_methods.items():
            self.deposit_api.create_deposition = Mock(side_effect=DepositApiException("Failed to create deposition", 404))
            with self.assertRaises(DepositApiException) as context:
                call(**self.create_deposition_params)
            self.assertEqual(str(context.exception), "Failed to create deposition", "Exception message is not correct")

    def test_get_deposition_success(self):
        # Test deposition found
        self.deposit_api.rest_adapter.get = Mock(return_value=Mock(status_code=200, data=self.deposition_mocked_data))
        deposit = self.deposit_api.get_deposition(dep_id=self.dep_id)
        self.assertIsInstance(deposit, Deposit, "Deposition was not created successfully")
        self.assertEqual(deposit.dep_id, self.dep_id, "Deposit ID is not correct")

    def test_get_deposition_failure(self):
        # Test deposition not found
        self.deposit_api.rest_adapter.get = Mock(side_effect=DepositApiException("Page not found", 404))
        deposit = self.deposit_api.get_deposition(dep_id=self.dep_id)
        self.assertIsNone(deposit, "Failed to get deposition")

    def test_get_all_depositions_success(self):
        # Test find all depositions_success
        obj1, obj2, obj3 = [self.deposition_mocked_data.copy() for _ in range(3)]
        obj1["id"] = "D_8233000014"
        obj2["id"] = "D_8233000015"
        obj3["id"] = "D_8233000016"
        self.deposit_api.rest_adapter.get = Mock(return_value=Mock(status_code=200, data={'total': 3, "items": [obj1, obj2, obj3]}))
        depositions = self.deposit_api.get_all_depositions()
        self.assertEqual(len(depositions), 3, "Number of depositions is incorrect")
        self.assertEqual(depositions[0].dep_id, "D_8233000014", "Deposit ID is not correct")
        self.assertEqual(depositions[1].dep_id, "D_8233000015", "Deposit ID is not correct")
        self.assertEqual(depositions[2].dep_id, "D_8233000016", "Deposit ID is not correct")

    def test_add_single_user(self):
        # Test addition of a single user
        self.deposit_api.rest_adapter.post = Mock(return_value=Mock(status_code=200, data=[self.user]))
        users = self.deposit_api.add_user(self.dep_id, self.orcids[0])
        self.assertEqual(len(users), 1, "Number of users is incorrect")
        for user in users:
            self.assertIsInstance(user, Depositor, "User was not added successfully")
            self.assertEqual(user.id, self.user["id"], "Deposit ID is not correct")
            self.assertEqual(user.orcid, self.orcids[0], "Deposit ID is not correct")

    def test_add_multiple_users(self):
        # Test addition of a multiple users
        user1 = self.user.copy()
        user2 = self.user.copy()
        user2["id"] = 2
        user2["orcid"] = self.orcids[1]
        self.deposit_api.rest_adapter.post = Mock(return_value=Mock(status_code=200, data=[user1, user2]))
        users = self.deposit_api.add_user(self.dep_id, self.orcids[0])
        self.assertEqual(len(users), 2, "Number of users is incorrect")
        for i, user in enumerate(users):
            self.assertIsInstance(user, Depositor, "User was not added successfully")
            self.assertEqual(user.id, i + 1, "Deposit ID is not correct")
            self.assertEqual(user.orcid, self.orcids[i], "Deposit ID is not correct")

    def test_upload_file_success(self):
        _, file_path = tempfile.mkstemp()
        with open(file_path, "w") as fp:
            fp.write("test file content")

        expected_response = {"id": 1, "name": "test.mmcif", "type": "co-pdb", "created": "Thursday, April 21, 2023 14:30:00"}
        self.deposit_api.rest_adapter.post = Mock(return_value=Mock(status_code=200, data=expected_response))

        result = self.deposit_api.upload_file(dep_id=self.dep_id, file_path=file_path, file_type=FileType.PDB_COORD)
        self.assertIsInstance(result, DepositedFile, "File upload failed")
        self.assertEqual(result.id, 1, "File ID is not correct")
        self.assertEqual(result.name, "test.mmcif")
        self.assertEqual(result._type, FileType.PDB_COORD)

        os.remove(file_path)

    def test_upload_file_failed(self):
        self.deposit_api.rest_adapter.post = Mock(side_effect=DepositApiException("Invalid file", 404))
        with self.assertRaises(DepositApiException) as context:
            _result = self.deposit_api.upload_file(dep_id=self.dep_id, file_path="/not/exists/file.mmcif", file_type=FileType.PDB_COORD)  # noqa: F841
        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(str(context.exception), "Invalid input file", "Invalid input file")

    def test_get_files(self):
        data = {
            'errors': [],
            'warnings': [],
            'files': [
                {'name': 'sdasdsa.mcif', 'type': 'co-pdb', 'id': 40, 'created': 'Friday, April 21, 2023 12:03:58'},
                {'name': '8f2i.cifuwG7AvQT', 'type': 'co-pdb', 'id': 41, 'created': 'Friday, April 21, 2023 12:06:37'}
            ]
        }
        self.deposit_api.rest_adapter.get = Mock(return_value=Mock(status_code=200, data=data))
        files = self.deposit_api.get_files(self.dep_id)
        self.assertIsInstance(files, DepositedFilesSet)
        self.assertEqual(len(files), 2)
        self.assertEqual(files[0].id, 40)
        self.assertEqual(files[1].id, 41)

    def test_get_status(self):
        self.deposit_api.rest_adapter.get = Mock(return_value=Mock(status_code=200,
                                                                   data={'step': 'upload', 'action': 'submit', 'details': 'Upload type processed',
                                                                         'date': '2023-04-17T14:57:37.774921', 'status': 'running'}))
        status = self.deposit_api.get_status(self.dep_id)
        self.assertIsInstance(status, DepositStatus)
        self.assertEqual(status.status, "running")

    def test_process(self):
        self.deposit_api.rest_adapter.post = Mock(return_value=Mock(status_code=200,
                                                                    data={'step': 'upload', 'action': 'submit', 'details': 'Upload type processed',
                                                                          'date': '2023-04-17T14:57:37.774921', 'status': 'running'}))
        status = self.deposit_api.process(self.dep_id)
        self.assertIsInstance(status, DepositStatus)
        self.assertEqual(status.status, "running")

    def tearDown(self):
        # Clean up any resources used in the tests
        pass


if __name__ == '__main__':
    unittest.main()

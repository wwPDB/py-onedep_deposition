import unittest
from deposit.deposit_api import DepositApi
from deposit.models import Experiment, Deposit, Depositor
from deposit.enum import Country, EMSubType
from deposit.exceptions import DepositApiException
from unittest.mock import Mock

class DepositApiTests(unittest.TestCase):

    def setUp(self):
        self.deposit_api = DepositApi()
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
        for method, call in self.create_deposition_methods.items():
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
            self.assertEqual(user.id, i+1, "Deposit ID is not correct")
            self.assertEqual(user.orcid, self.orcids[i], "Deposit ID is not correct")






    def tearDown(self):
        # Clean up any resources used in the tests
        pass

if __name__ == '__main__':
    unittest.main()

"""
Unit Test Cases for Models.
"""
import datetime
from django.test import TestCase
from django.db import models
from .. import models as rentezzy_models


class TestModels(TestCase):
    """
    Class for defining unit test cases methods.
    """
    def setUp(self):
        """
        Constructor for each unit test case
        """
        class DummyModel(models.Model):
            """
            Assigns a manager for dummy test model.
            """
            objects = rentezzy_models.PaymentManager()

        self.DummyModel = DummyModel
        self.assertIsInstance(self.DummyModel.objects, rentezzy_models.PaymentManager)

    def test_model_str(self):
        """
        Unit test case for string format of model object.
        """
        room_obj = rentezzy_models.Rooms.objects.create(
            start_date=datetime.date.today(),
            end_date=datetime.date.today(),
            county="Limerick",
            eir_code="V94PK66",
            monthly_rent_amount=500,
            deposit_amount=500,
            total_amount=1000,
            property_age=5
        )
        self.assertEqual(str(room_obj), "V94PK66 - Limerick")

"""
Unit Test Cases for Views.
"""
import datetime
from django.test import TestCase, Client
from .. import models


class TestViews(TestCase):
    """
    Class for defining unit test cases methods.
    """
    def setup(self):
        """
        Constructor for each unit test case
        """
        self.client = Client()

    def test_search_room(self):
        """
        Unit Test case for search_room view.
        """
        response = self.client.get("/rent/search_room")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/index.html")

    def test_delete_room(self):
        """
        Unit Test case for delete_room view.
        """
        models.Rooms.objects.create(
            start_date=datetime.date.today(),
            end_date=datetime.date.today(),
            county="Limerick",
            monthly_rent_amount=500,
            deposit_amount=500,
            total_amount=1000,
            property_age=5
        )
        self.client.login(username="21136467@studentmail.ul.ie", password="admin")
        response = self.client.post("/rent/delete_room", {"user": "Owner", "id": 1})

        self.assertEqual(response.status_code, 302)

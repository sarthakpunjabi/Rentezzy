"""
Unit Test Cases for Urls.
"""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .. import views


class TestUrls(SimpleTestCase):
    """
    Class for defining unit test cases methods.
    """
    def test_add_room_is_resolved(self):
        """
        Unit test case for add_room url.
        """
        url = reverse("add_room")
        self.assertEqual(resolve(url).func, views.add_room)

    def test_delete_room_is_resolved(self):
        """
        Unit test case for delete_room url.
        """
        url = reverse("delete_room")
        self.assertEqual(resolve(url).func, views.delete_room)

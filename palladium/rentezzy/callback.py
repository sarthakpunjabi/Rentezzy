"""
Implementation of observer for updating price with discount
"""

from datetime import date, timedelta
from . import models, factory


def notify_user():
    """
    Dummy Observer Implemented for demonstration of Observer Design Pattern
    """
    print("In side notify user")


def update_price():
    """
    This observer update the price with discount for Old age and intermediate age properties
    """
    threshold_date = date.today() - timedelta(days=15)
    rooms_obj = models.Rooms.objects.filter(created_at__lte=threshold_date)

    discount_factory = factory.DiscountFactory()
    for room in rooms_obj:
        discounted_price = discount_factory.add_discount(room.deposit_amount, room.property_age)
        room.deposit_amount = discounted_price
        room.save()

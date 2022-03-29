"""Validation file"""
from datetime import date
from . import models as rentezzy_models


class Validators:
    """
    Validator class consist of function with respect to field and it validation
    """

    @staticmethod
    def start_date_validation(request_details):
        """
        This function takes in the request and do the start date validation.
        it returns false in case of validation error,otherwise returns true.
        """
        start_date = request_details.get("start_date")
        present_date = date.today()
        if start_date < present_date:
            return False
        if not start_date:
            return False
        return True

    @staticmethod
    def end_date_validation(request_details):
        """
        This function takes in the request and do the end date validation.
        it returns false in case of validation error,otherwise returns true.
        """
        start_date = request_details.get("start_date")
        end_date = request_details.get("end_date")
        present_date = date.today()
        if present_date > start_date > end_date:
            return False
        if not end_date:
            return False
        return True

    @staticmethod
    def eir_code_validation(request_details):
        """
        This function takes in the request and do the eir code (length) validation.
        it returns false in case of validation error,otherwise returns true.
        """
        eir_code = request_details.get("eir_code")
        if len(eir_code) == 7:
            return True
        return False

    @staticmethod
    def monthly_rent_amount_validation(request_details):
        """
        This function takes in the request and do the monthly rent amount validation.
        it returns false in case of validation error,otherwise returns true.
        """
        monthly_rent_amount = request_details.get("monthly_rent_amount")
        if monthly_rent_amount == 0:
            return False
        if not monthly_rent_amount:
            return False
        return True

    @staticmethod
    def deposit_amount_validation(request_details):
        """
        This function takes in the request and do the deposit amount validation.
        it returns false in case of validation error,otherwise returns true.
        """
        deposit_amount = request_details.get("deposit_amount")
        if deposit_amount == 0:
            return False
        if not deposit_amount:
            return False
        return True

    @staticmethod
    def property_age_validation(request_details):
        """
        This function takes in the request and do the property age validation.
        it returns false in case of validation error,otherwise returns true.
        """
        property_age = request_details.get("property_age")
        if not property_age:
            return False
        return True


class CancelBookingValidator:
    """
    CancelBookingValidator consists of methods use for validating cancellation of booking fields.
    """
    @staticmethod
    def date_validation(room_id):
        """
        This method takes the room_id as checks if the start_date of the property
        is more than cancellation request date.
        """
        booking_obj = rentezzy_models.Booking.objects.get(room__id=room_id)
        if booking_obj.cancellation_date:
            print("Room Already cancelled")
            return False

        # Currently user can cancel the booking of room,
        # Cancellation should be before the start date of room rental agreement.
        if date.today() >= booking_obj.start_date:
            return False

        return True

    @staticmethod
    def status_validation(room_id):
        """
        This method checks the status, and validates if the cancel request is for
        already cancelled booking.
        """
        booking_obj = rentezzy_models.Booking.objects.get(room__id=room_id)
        if booking_obj.room.status == "Available" or booking_obj.payments == "Returned":
            return False

        return True

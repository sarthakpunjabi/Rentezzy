"""
This holds the integration of payment gateways in our application.
"""
import uuid


class VisaMode:
    """
    Integration of Visa payment gateway.
    """
    def __init__(self, payment_obj):
        self.payment_obj = payment_obj

    def pay(self, dummy_flag=True):
        """
        Method of Paying the amount.
        """
        if dummy_flag:
            return {
                "status": "success",
                "reason": "",
                "total_price": self.payment_obj.get("price"),
                "amt_received": self.payment_obj.get("amount"),
                "currency": self.payment_obj.get("currency"),
                "source": "VISA",
                "orderId": uuid.uuid4()
            }
        # If dummy flag is not set, return a dummy response.
        return {
            "status": "fail",
            "reason": "Dummy Reason for Failure",
            "total_price": self.payment_obj.get("price"),
            "amt_received": 0,
            "currency": self.payment_obj.get("currency"),
            "source": "VISA",
            "orderId": None
        }


class MasterCardMode:
    """
    Integration of MasterCard payment gateway.
    """
    def __init__(self, payment_obj):
        self.payment_obj = payment_obj

    def pay(self, dummy_flag=True):
        """
        Method of Paying the amount.
        """
        if dummy_flag:
            return {
                "status": "success",
                "reason": "",
                "total_price": self.payment_obj.get("price"),
                "amt_received": self.payment_obj.get("amount"),
                "currency": self.payment_obj.get("currency"),
                "source": "MASTERCARD",
                "orderId": uuid.uuid4()
            }
        # If dummy flag is not set, return a dummy response.
        return {
            "status": "fail",
            "reason": "Dummy Reason for Failure",
            "total_price": self.payment_obj.get("price"),
            "amt_received": 0,
            "currency": self.payment_obj.get("currency"),
            "source": "MASTERCARD",
            "orderId": None
        }

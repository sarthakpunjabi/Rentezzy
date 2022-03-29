"""
This implements the factory interface for Rentezzy Application.
"""
from . import state_pattern, validator, payment_modes


class PaymentFactory:
    """
    Factory class for determining payment methods.
    """
    def __init__(self):
        pass

    @staticmethod
    def choose_operator(payment_obj):
        """
        Method for selecting the concrete function for payment.
        """
        target_class = payment_obj.get("type") + "Mode"
        return getattr(payment_modes, target_class)(payment_obj)


class ValidatorFactory:
    """
    Factory class for determining Validation methods.
    """
    def __init__(self):
        pass

    @staticmethod
    def validate(request_details):
        """
        Method for selecting the concrete function for validating the request data.
        """
        method_list = [
            method
            for method in dir(validator.Validators)
            if method.endswith('_validation') is True
        ]
        for method in method_list:
            validate = validator.Validators()
            return getattr(validate, method)(request_details)
        return True

    @staticmethod
    def validate_cancel_booking(room_id):
        """
        Method for selecting the concrete function for validating request data.
        """
        method_list = [
            method
            for method in dir(validator.CancelBookingValidator)
            if method.endswith('_validation') is True
        ]
        for method in method_list:
            validate = validator.CancelBookingValidator()
            return getattr(validate, method)(room_id)
        return True


class AgentCommissionFactory:
    """
    Factory class for calculating Agent commission.
    """
    def __init__(self):
        pass

    @staticmethod
    def calculate_commission(agent_level, rooms):
        """
        Method for selecting the concrete function for calculating commission.
        """
        target_state = agent_level.title() + "State"
        # Check if the agent is a Platinum Agent depending on number of room booked
        if agent_level != "Platinum" and len(rooms) > 10:
            target_state = "PlatinumState"
        agent = state_pattern.AgentState()
        state = getattr(state_pattern, target_state)()
        agent.set_state(state)
        return agent.calculate_commission(rooms)


class DiscountFactory:
    """
    Factory class for calculating discount on rental properties.
    """
    def __init__(self):
        pass

    @staticmethod
    def add_discount(actual_price, age):
        """
        Method for selecting the concrete function for calculating discount.
        """
        level = "OldAge"
        if 10 < age < 25:
            level = "IntermediateAge"
        target_state = level + "Room"
        discount = state_pattern.DiscountState()
        state = getattr(state_pattern, target_state)()
        discount.set_state(state)
        return discount.calculate_discount(actual_price)

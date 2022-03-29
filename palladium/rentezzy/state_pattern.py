"""
This holds the State Design Pattern implemented in rentezzy application.
"""
from abc import abstractmethod, ABCMeta


class InternalState(metaclass=ABCMeta):
    """
    Parent Class for calculating the commission.
    """
    def __init__(self):
        pass

    @abstractmethod
    def calculate_commission(self, rooms):
        """
        Parent method for calculating base commission logic.
        """
        pass

    @staticmethod
    def calc_total_room_price(rooms):
        """
        Parent Method for calculating commission
        """
        price = 0
        for room in rooms:
            price += room.monthly_rent_amount
        return price


class GoldState(InternalState):
    """
    Type for Level achieved for commission.
    """
    def __init__(self):
        super().__init__()

    def calculate_commission(self, rooms):
        """
        Method for calculating commission.
        """
        price = super().calc_total_room_price(rooms)
        # Keeping the Multiplicity Factor in Gold Level as 0.050
        return 0.050 * price


class PlatinumState(InternalState):
    """
    Type for Level achieved for commission.
    """
    def __init__(self):
        super().__init__()

    def calculate_commission(self, rooms):
        """
        Method for calculating commission.
        """
        # Keeping the Multiplicity Factor in Platinum Level as 0.075
        price = super().calc_total_room_price(rooms)
        return 0.075 * price


class AgentState(InternalState):
    """
    State Class
    """
    def __init__(self):
        super().__init__()
        self.state = None

    def set_state(self, status):
        """
        Setter for passing an object
        """
        self.state = status

    def get_state(self):
        """
        Getter for fetching an object.
        """
        return self.state

    def calculate_commission(self, rooms):
        """
        Calculates commission, based on the type of object passed in setter.
        """
        return self.state.calculate_commission(rooms)


class Discount(metaclass=ABCMeta):
    """
    Parent Class for calculating the discount.
    """
    def __init__(self):
        pass

    @abstractmethod
    def calculate_discount(self, actual_price):
        """
        Parent method for calculating base discount logic.
        """
        pass

    @staticmethod
    def calc_total_room_price(actual_price, discount):
        """
        Parent Method for calculating the discount.
        """
        return actual_price - discount


class OldAgeRoom(Discount):
    """
    Discount based on age of property.
    """
    def calculate_discount(self, actual_price):
        """
        Calculates discount based on age of property.
        """
        discount = 0.10 * actual_price
        # Keeping the Multiplicity Factor in Gold Level as 0.10
        return super().calc_total_room_price(actual_price, discount)


class IntermediateAgeRoom(Discount):
    """
    Discount based on age of property.
    """
    def calculate_discount(self, actual_price):
        """
        Calculates discount based on age of property.
        """
        discount = 0.05 * actual_price
        # Keeping the Multiplicity Factor in Platinum Level as 0.05
        return super().calc_total_room_price(actual_price, discount)


class DiscountState(Discount):
    """
    State Class
    """
    def __init__(self):
        super().__init__()
        self.state = None

    def set_state(self, status):
        """
        Setter for fetching an object.
        """
        self.state = status

    def get_state(self):
        """
        Getter for fetching an object.
        """
        return self.state

    def calculate_discount(self, actual_price):
        """
        Calculates Discount, based on the type of object passed in setter.
        """
        return self.state.calculate_discount(actual_price)

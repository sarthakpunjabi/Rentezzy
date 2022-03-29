"""
It holds the schema of Rentezzy Database.
It contains the essential fields and behaviors of the data
"""
import datetime
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from Loginsystem.models import NewUser


USER_TYPE = (
    ("CUSTOMER", "Customer"),
    ("AGENT", "Agent"),
    ("OWNER", "Owner"),
)

STATUS_TYPE = (
    ("AVAILABLE", "Available"),
    ("TAKEN", "Taken"),
    ("ONHOLD", "OnHold"),
    ("BOOKED", "Booked"),
    ("DELETED", "Deleted"),
)

COUNTY_TYPE = (
    ("None", "None"),
    ("Carlow", "Carlow"),
    ("Cavan", "Cavan"),
    ("Clare", "Clare"),
    ("Cork", "Cork"),
    ("Donegal", "Donegal"),
    ("Dublin", "Dublin"),
    ("Galway", "Galway"),
    ("Kerry", "Kerry"),
    ("Kildare", "Kildare"),
    ("Kilkenny", "Kilkenny"),
    ("Laois", "Laois"),
    ("Leitrim", "Leitrim"),
    ("Limerick", "Limerick"),
    ("Longford", "Longford"),
    ("Louth", "Louth"),
    ("Mayo", "Mayo"),
    ("Meath", "Meath"),
    ("Monaghan", "Monaghan"),
    ("Offaly", "Offaly"),
    ("Roscommon", "Roscommon"),
    ("Sligo", "Sligo"),
    ("Tipperary", "Tipperary"),
    ("Waterford", "Waterford"),
    ("Westmeath", "Westmeath"),
    ("Wexford", "Wexford"),
    ("Wicklow", "Wicklow"),
)

PAYMENT_TYPE = (
    ("VISA", "Visa"),
    ("MASTERCARD", "MasterCard"),
)

PAYMENT_STATUS = (
    ("SUCCESS", "Success"),
    ("FAILED", "Failed"),
    ("RETURNED", "Returned"),
)


def validate_length(value):
    """
    Custom Validator for validating length.
    """
    if len(value) != 7:
        raise ValidationError(_('EIR code %(value) is not correctly entered'),
                              params={'value': value}, )


class RoomDetails(models.Model):
    """
    RoomDetails schema.
    """
    # Owner or Agent Only
    user = models.OneToOneField(NewUser, null=True, blank=True, on_delete=models.SET_NULL)
    type = models.CharField(max_length=10, choices=USER_TYPE, blank=True, null=True)
    enquiry_email = models.CharField(max_length=220)

    class Meta:
        """
        Meta Class
        """
        verbose_name_plural = "Room Details"


class PaymentManager(models.Manager):
    """
    Manages method for Payment DB Schema.
    """
    def create_payment(self, payment_details):
        """
        Method for creating payment
        """
        return self.create(
            total_price=payment_details.get("total_price"),
            amt_received=payment_details.get("amt_received"),
            currency=payment_details.get("currency"),
            source=payment_details.get("source"),
            orderId=payment_details.get("orderId", None),
            failure_reason=payment_details.get("reason"),
            # Only one status will match
            status=[
                status[1]
                for status in PAYMENT_STATUS
                if payment_details.get("status") in status[0].lower()
            ][0]
        )

    def update_payment_status(self, order_id, status):
        """
        Method for updating payment status
        """
        payment_obj = self.get(orderId=order_id)
        payment_obj.status = status
        payment_obj.save()


class Payments(models.Model):
    """
    Payment Schema.
    """
    application_commission = models.IntegerField
    total_price = models.IntegerField()
    amt_received = models.IntegerField()
    currency = models.CharField(max_length=50)
    source = models.CharField(max_length=10, choices=PAYMENT_TYPE, default="Visa")
    orderId = models.UUIDField(default=None, blank=True, null=True)
    failure_reason = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS)

    class Meta:
        """
        Meta Class
        """
        verbose_name_plural = "Payments"

    objects = PaymentManager()


class RoomManager(models.Manager):
    """
    Manages method for Room's DB Schema.
    """
    @staticmethod
    def get_total_rent_due(start_date, end_date, monthly_rent_amount, deposit_amount):
        """
        Method for getting total rent.
        """
        num_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
        if num_months == 0:
            return monthly_rent_amount + deposit_amount

        total_rent = num_months * monthly_rent_amount
        total_amount = total_rent + deposit_amount
        return total_amount

    def get_available_rooms(self, county=None):
        """
        Method for fetching the list of available rooms.
        """
        room_obj = self.filter(status__in=["AVAILABLE", "Available"])
        if county:
            room_obj = room_obj.filter(county__icontains=county)
        return room_obj

    def update_room_status(self, room_id, status):
        """
        Method for updating the status of the room.
        """
        try:
            room_obj = self.get(id=room_id)
            room_obj.status = status
            room_obj.save()
        except self.model.DoesNotExist:
            return None
        return room_obj

    @staticmethod
    def subtract_amount(amount, room_obj):
        """
        Method for subtracting the amount.
        """
        if amount:
            room_obj.total_amount -= amount
            room_obj.save()

    def add_room(self, data, user):
        """
        Method for adding the room.
        """
        try:
            # Will get from the request, since we are using decorator
            room_detail = RoomDetails.objects.create(
                type=user.type,
                enquiry_email=user.email,
            )
            room_detail.user = user
            room_detail.save()
            self.create(
                start_date=data.get("start_date"),
                end_date=data.get("end_date"),
                eir_code=data.get("eir_code"),
                address=data.get("address"),
                county=data.get("county"),
                contract_details=data.get("contract_details"),
                monthly_rent_amount=data.get("monthly_rent_amount"),
                deposit_amount=data.get("deposit_amount"),
                total_amount=self.get_total_rent_due(
                    data.get("start_date"),
                    data.get("end_date"),
                    data.get("monthly_rent_amount"),
                    data.get("deposit_amount")
                ),
                room_details=room_detail,
                image_url=data.get("image_url"),
                img1=data.get("img1"),
                img2=data.get("img2"),
                img3=data.get("img3"),
                video_url=data.get("video_url"),
                status=data.get("status"),
                property_age=data.get("property_age")
            )
        except ValidationError as err:
            print("Error while adding room", err)

    def get_agent_bookings(self, agent):
        """
        Method for getting the agent booking.
        """
        return self.filter(status="AVAILABLE", room_details__user=agent)


class Rooms(models.Model):
    """
    Rooms Schema.
    """
    start_date = models.DateField()
    end_date = models.DateField()
    eir_code = models.CharField(max_length=7, validators=[validate_length])
    address = models.CharField(max_length=100)
    county = models.CharField(max_length=10, choices=COUNTY_TYPE, default="None")
    contract_details = models.FileField(upload_to='media/', blank=True, null=True)
    monthly_rent_amount = models.IntegerField()
    deposit_amount = models.IntegerField()
    total_amount = models.IntegerField()
    description = models.CharField(max_length=500,default="this is description")
    room_details = models.OneToOneField(RoomDetails, on_delete=models.CASCADE, null=True, blank=True)
    room_details = models.OneToOneField(
        RoomDetails,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    image_url = models.FileField(upload_to='media/', blank=True, null=True)
    img1 = models.ImageField(upload_to='media/', blank=True, null=True)
    img2 = models.ImageField(upload_to='media/', blank=True, null=True)
    img3 = models.ImageField(upload_to='media/', blank=True, null=True)
    video_url = models.FileField(upload_to='media/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_TYPE, default="Available")
    property_age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = RoomManager()

    def __str__(self):
        return "{} - {}".format(self.eir_code, self.county)

    class Meta:
        """
        Meta Class
        """
        verbose_name_plural = "Rooms"


class BookManager(models.Manager):
    """
    Manages method for Booking DB Schema.
    """
    def create_booking(self, payment_obj, room_obj, user):
        """
        Method to create booking.
        """
        self.create(
            start_date=room_obj.start_date,
            end_date=room_obj.end_date,
            deposit_details=room_obj.deposit_amount,
            payments=payment_obj,
            room=room_obj,
            user=user
        )

    def get_booking(self, room_obj, user):
        """
        Method for getting the user booking.
        """
        return self.get(room=room_obj, user=user)

    def cancel_booking(self, room_obj):
        """
        Method for cancelling the booking.
        """
        try:
            booking_obj = self.get(room=room_obj)
        except self.model.DoesNotExist:
            return None
        booking_obj.cancellation_date = datetime.date.today()
        booking_obj.save()
        return booking_obj

    def fetch_bookings(self, user):
        """
        Method for fetching user bookings.
        """
        return self.filter(user=user).values("room__county", "room__id", "room__status")


class Booking(models.Model):
    """
    Booking Schema.
    """
    user = models.ForeignKey(NewUser, blank=True, null=True, on_delete=models.SET_NULL)
    start_date = models.DateField()
    end_date = models.DateField()
    deposit_details = models.IntegerField()
    payments = models.OneToOneField(Payments, on_delete=models.CASCADE, blank=True, null=True)
    cancellation_date = models.DateField(blank=True, null=True)
    room = models.OneToOneField(Rooms, on_delete=models.CASCADE, blank=True, null=True)

    objects = BookManager()

    def __str__(self):
        return "{}".format(self.start_date)


class Commission(models.Model):
    """
    Commission Schema.
    """
    # Agents only
    User = models.OneToOneField(NewUser, blank=True, null=True, on_delete=models.SET_NULL)
    number_of_rooms_booked = models.IntegerField()
    commission_amt = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Ratings(models.Model):
    """
    Ratings Schema.
    """
    user = models.OneToOneField(NewUser, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField()
    commented = models.TextField(max_length=500)
    room = models.OneToOneField(Rooms, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Contact(models.Model):
    """
    Contact agent and owner
    """
    full_name = models.CharField(max_length=100)
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(max_length=200,null=True,blank=True)
    Description = models.CharField(max_length=400)
    room_details = models.OneToOneField(RoomDetails, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        returning name
        """
        return f'{self.full_name}'
'''Creating multiple roles and custom user model'''
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _

SUBSCRIPTION_CHOICES = (
    ("NONE", "None"),
    ("GOLD", "Gold"),
    ("SILVER", "Silver"),
    ("PLATINUM", "Platinum"),
)

USER_TYPE = (
    ("CUSTOMER", "Customer"),
    ("AGENT", "Agent"),
    ("OWNER", "Owner"),
)

AGENT_LEVEL = (
    ("GOLD", "Gold"),
    ("PLATINUM", "Platinum"),
)


# Create your models here.
class CustomAccountManager(BaseUserManager):
    '''Custom Account manager for managing roles'''
    ordering = ('email',)

    def create_user(self, email, first_name, last_name, password, **other_fields):
        '''Defining and creating user function'''
        if not email:
            raise ValueError(_("Email Is Mandatory"))
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password, **other_fields):
        '''Defining and creating superuser function'''
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)
        other_fields.setdefault("is_staff", True)
        return self.create_user(email, first_name, last_name, password, **other_fields)


class Subscription(models.Model):
    '''adding sucscription model for agent and customer'''
    start_date = models.DateField()
    end_date = models.DateField()
    type = models.CharField(max_length=20, choices=SUBSCRIPTION_CHOICES, default="None")
    number_of_property = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NewUser(AbstractBaseUser, PermissionsMixin):
    '''Adding custom user models and permission'''
    class Types(models.TextChoices):
        '''Creating Proxy types and giving choices'''
        CUSTOMER = "CUSTOMER", "Customer"
        AGENT = "AGENT", "Agent"
        OWNER = "OWNER", "Owner"

    type = models.CharField(_('Type'), max_length=50, choices=Types.choices, default=Types.CUSTOMER)

    user_name = models.CharField(max_length=150,unique=False)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=200)
    subscription = models.BooleanField(default=False)
    subscription_details = models.OneToOneField(Subscription,
     on_delete=models.CASCADE,
      null=True, blank=True,
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    level = models.CharField(max_length=20, choices=AGENT_LEVEL, default="GOLD")
    # booking_history is not needed, as we can get this details by querying room details
    objects = CustomAccountManager()
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        '''Returning str function'''
        return f"{self.first_name}"

    def get_absolute_url(self):
        '''Reverse url for error 404'''
        return "/users/%i/" % (self.pk)


class CustomerManager(models.Manager):
    '''this is the manager for customer type role'''
    def get_queryset(self, *args, **kwargs):
        '''Returning querysets of proxy model customer'''
        return super().get_queryset(*args, **kwargs).filter(type=NewUser.Types.CUSTOMER)

    def save(self, *args, **kwargs):
        '''Overriding the save function '''
        if not self.pk:
            self.type = NewUser.Types.CUSTOMER
        return super().save(*args, **kwargs)


class OwnerManager(models.Manager):
    '''this is the manager for owner type role'''
    def get_queryset(self, *args, **kwargs):
        '''Returning querysets of proxy model Owner'''
        return super().get_queryset(*args, **kwargs).filter(type=NewUser.Types.OWNER)

    def save(self, *args, **kwargs):
        '''Overriding the save function '''
        if not self.pk:
            self.type = NewUser.Types.OWNER
        return super().save(*args, **kwargs)


class AgentManager(models.Manager):
    '''this is the manager for agent type role'''
    def get_queryset(self, *args, **kwargs):
        '''Returning querysets of proxy model agent'''
        return super().get_queryset(*args, **kwargs).filter(type=NewUser.Types.AGENT)

    def save(self, *args, **kwargs):
        '''Overriding the save function '''
        if not self.pk:
            self.type = NewUser.Types.AGENT
        return super().save(*args, **kwargs)


class Customer(NewUser):
    '''this is proxy model for customer for fast and async models'''
    objects = CustomAccountManager()

    class Meta:
        '''obligating meta as true'''
        proxy = True


class Owner(NewUser):
    '''this is proxy model for Owner for fast and async models'''
    objects = OwnerManager()

    class Meta:
        '''obligating meta as true'''
        proxy = True

class Agent(NewUser):
    '''this is proxy model for Agemt for fast and async models'''
    objects = AgentManager()

    class Meta:
        '''obligating meta as true'''
        proxy = True

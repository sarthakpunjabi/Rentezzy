""" Forms for Crud system"""
from django import forms
from .models import Rooms,Booking


class RoomForm(forms.ModelForm):
    """
    Room form
    """
    class Meta:
        """
        META CLASS
        """
        model = Rooms
        fields = '__all__'


class BookingForm(forms.ModelForm):
    """
    Booking form 
    """
    class Meta:
        """
        META CLASS
        """
        model = Booking
        fields = '__all__'
        
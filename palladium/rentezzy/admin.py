"""
This holds the configuration for our admin dashboard.
"""
from django.contrib import admin
from . import models

admin.site.site_header = 'RentEzzy'
admin.site.register(models.Rooms)
admin.site.register(models.RoomDetails)
admin.site.register(models.Booking)
admin.site.register(models.Payments)
admin.site.register(models.Commission)
admin.site.register(models.Ratings)
admin.site.register(models.Contact)
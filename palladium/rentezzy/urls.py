"""
This file consists of all the URL's used by rentezzy application.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('add_room', views.add_room, name="add_room"),
    path('delete_room', views.delete_room, name="delete_room"),
    path('book_room', views.book_room, name="book_room"),
    path('search_room/', views.search_rooms, name="search_room"),
    path('search_room/<int:room_id>/', views.detail_room, name="detail_room"),
    path('search_room/<int:room_id>/contact', views.contact_room, name="contact"),
    path('fetch_booking', views.get_booked_room, name="fetch_booking"),
    path('cancel_booking', views.cancel_booking, name="cancel_booking"),
    path('get_agent_commission', views.get_agent_commission, name="get_agent_commission"),
    path('discount_batch', views.add_discount, name="add_discount"),
]

from django.urls import path
from . import views

urlpatterns = [
    path('flight_list/', views.flight_list, name='flight_list'),
    path('airports/', views.airports, name='airports'),
    path('flight/', views.flight, name='flight'),
    path('flight/<str:flight_id>/', views.get_flight, name='get_flight'),
    path('book/<str:flight_id>/', views.add_booking, name='book'),
    path('delete/<str:booking_id>/', views.delete_booking, name='delete_booking'),
    path('pay/<str:booking_id>/', views.pay, name='pay'),
    path('booking_details/<str:booking_id>/', views.get_booking_details, name='get_booking_details'),
]


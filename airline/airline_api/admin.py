from django.contrib import admin
from .models import Flight, Airport, Booking, Customer, Seat, FlightSeat

admin.site.register(Flight)
admin.site.register(Airport)
admin.site.register(Booking)
admin.site.register(Customer)
admin.site.register(Seat)
admin.site.register(FlightSeat)
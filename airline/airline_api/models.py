from django.db import models
import uuid
from jsonfield import JSONField

class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    flight = models.ForeignKey('Flight', on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='bookings',null=True)
    price = models.FloatField()
    insurance = models.BooleanField()
    status = models.CharField(max_length=50)
    start_time = models.DateTimeField()

class Flight(models.Model):
    id = models.AutoField(primary_key=True)
    origin = models.ForeignKey('Airport', on_delete=models.CASCADE, related_name='departures')
    destination = models.ForeignKey('Airport', on_delete=models.CASCADE, related_name='arrivals')
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    duration = models.DurationField()
    plane_type = models.CharField(max_length=50)
    number_of_seats = models.IntegerField()
    price = models.IntegerField(default=0)
    seats = models.ManyToManyField('Seat', through='FlightSeat', related_name='flights')

class Seat(models.Model):
    id = models.AutoField(primary_key=True)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='flight_seats',default=1)
    category = models.CharField(max_length=10, default='economy')
    price = models.IntegerField(blank=True, null=True)
    number = models.CharField(max_length=10, blank=True, null=True)
    available = models.CharField(max_length=10, blank=True,null=True)

class FlightSeat(models.Model):
    flight = models.ForeignKey('Flight', on_delete=models.CASCADE)
    seat = models.ForeignKey('Seat', on_delete=models.CASCADE)

class Airport(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    code = models.CharField(max_length=10)
    country = models.CharField(max_length=10)
    terminals = models.IntegerField()

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE, related_name='customers', null=True)
    first_name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    seat = models.ForeignKey('Seat', on_delete=models.CASCADE, null=True)
    luggage = JSONField()
    passport = models.IntegerField()
from django.shortcuts import render
from django.http import JsonResponse, Http404, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import Flight, Airport, Booking, Customer
import json
from datetime import datetime

@csrf_exempt
def flight_list(request):
    if(request.method== 'GET'):
        flights = Flight.objects.all()
        flightArr = []
        luggageDict = {
        "cabin": 0.0,
        "carry-on": 20.0,
        "checked-in": 30.0
        }
        for flight in flights:  
            seats_on_flight = flight.seats.all()
            seat_list = []
            for seat in seats_on_flight:
                seat_dict = {
                    "seat_id": seat.id,
                    "seat_name":seat.number,
                    'class': seat.category,
                    'price': seat.price,
                    'status': seat.available
                }
                seat_list.append(seat_dict)
            
            my_origin = {
            'id': flight.origin.id,
            'name': flight.origin.name,
            'code': flight.origin.code,
            'city': flight.origin.city,
            'terminals': flight.origin.terminals,
            'country': flight.origin.country
            }
            
            my_destination = {
            'id': flight.destination.id,
            'name': flight.destination.name,
            'code': flight.destination.code,
            'city': flight.destination.city,
            'terminals': flight.destination.terminals,
            'country': flight.destination.country
            }

            duration_in_minutes = int(flight.duration.total_seconds()//60)
            flightArr.append({
            'flight_id': flight.id,
            'airline': "New Airline",
            'origin': my_origin,
            'destination': my_destination,
            'departure_time': flight.departure_time,
            'duration': duration_in_minutes,
            'arrival_time': flight.departure_time+flight.duration,
            'seats': seat_list,
            'plane_type': flight.plane_type,
            'price': flight.price,
            'insurance_price': 15,
            'priority_price': 10,
            'luggage_pricing': luggageDict,
            })
            return JsonResponse({"flights":flightArr}, safe=False)

@csrf_exempt
def airports(request):
    airports = Airport.objects.all()
    airArr = []
    for airport in airports:
        airArr.append({
            'id': airport.id,
            'name': airport.name,
            'code': airport.code,
            'city': airport.city,
            'terminals': airport.terminals,
            'country': airport.country
        })
    return JsonResponse(airArr, safe=False)

@csrf_exempt
def get_flight(request, flight_id):
    try:
        flight = Flight.objects.get(id=flight_id)
    except Flight.DoesNotExist:
        raise Http404("Flight not found")
    luggageDict = {
        "cabin": 0.0,
        "carry-on": 20.0,
        "checked-in": 30.0
    }

    seats_on_flight = flight.seats.all()
    seat_list = []
    for seat in seats_on_flight:
        seat_dict = {
            "seat_id": seat.id,
            "seat_name":seat.number,
            'class': seat.category,
            'price': seat.price,
            'status': seat.available
        }
        seat_list.append(seat_dict)
    
    my_origin = {
    'id': flight.origin.id,
    'name': flight.origin.name,
    'code': flight.origin.code,
    'city': flight.origin.city,
    'terminals': flight.origin.terminals,
    'country': flight.origin.country
    }
    
    my_destination = {
    'id': flight.destination.id,
    'name': flight.destination.name,
    'code': flight.destination.code,
    'city': flight.destination.city,
    'terminals': flight.destination.terminals,
    'country': flight.destination.country
    }
    
    duration_in_minutes = int(flight.duration.total_seconds()//60)
    found_flight = {
    'flight_id': flight.id,
    'airline': "New Airline",
    'origin': my_origin,
    'destination': my_destination,
    'departure_time': flight.departure_time,
    'duration': duration_in_minutes,
    'arrival_time': flight.departure_time+flight.duration,
    'seats': seat_list,
    'plane_type': flight.plane_type,
    'price': flight.price,
    'insurance_price': 15,
    'priority_price': 10,
    'luggage_pricing': luggageDict,
    }
    return JsonResponse(found_flight, safe=False)

@csrf_exempt
def flight(request):
    try:
        data = json.loads(request.body)
        origin = data['origin']
        destination = data['destination']
        departure_date_str = data['departure_date']
        departure_date = datetime.strptime(departure_date_str, '%Y-%m-%d').date()
        number_of_people = data['number_of_people']
    except (KeyError, ValueError):
        return HttpResponseBadRequest('Required fields not satisfied')
    flights = Flight.objects.all()
    luggageDict = {
        "cabin": 0.0,
        "carry-on": 20.0,
        "checked-in": 30.0
        }

    for flight in flights:  
        if(flight.origin.code==origin and flight.destination.code==destination):
            if(flight.departure_time.date()==departure_date and flight.number_of_seats > number_of_people):
                seats_on_flight = flight.seats.all()
                seat_list = []
                for seat in seats_on_flight:
                    seat_dict = {
                        "seat_id": seat.id,
                        "seat_name":seat.number,
                        'class': seat.category,
                        'price': seat.price,
                        'status': seat.available
                    }
                    seat_list.append(seat_dict)
                
                my_origin = {
                'id': flight.origin.id,
                'name': flight.origin.name,
                'code': flight.origin.code,
                'city': flight.origin.city,
                'terminals': flight.origin.terminals,
                'country': flight.origin.country
                }
                
                my_destination = {
                'id': flight.destination.id,
                'name': flight.destination.name,
                'code': flight.destination.code,
                'city': flight.destination.city,
                'terminals': flight.destination.terminals,
                'country': flight.destination.country
                }
                
                duration_in_minutes = int(flight.duration.total_seconds()//60)
                found_flight = {
                'flight_id': flight.id,
                'airline': "New Airline",
                'origin': my_origin,
                'destination': my_destination,
                'departure_time': flight.departure_time,
                'duration': duration_in_minutes,
                'arrival_time': flight.departure_time+flight.duration,
                'seats': seat_list,
                'plane_type': flight.plane_type,
                'price': flight.price,
                'insurance_price': 15,
                'priority_price': 10,
                'luggage_pricing': luggageDict,
                }
                return JsonResponse(found_flight, safe=False)
    raise Http404("Flight not found")
    
            

@csrf_exempt
def add_booking(request,flight_id):
    if request.method == 'POST':
        idArr = []
        try:
            data = json.loads(request.body)
            passengers = data['passengers']
            insurance = data['insurance']
            priority = data['priority']
        except (KeyError, ValueError):
            return HttpResponseBadRequest('Invalid or missing parameters')
        try:
            flight = Flight.objects.get(id=flight_id)
            all_seats = flight.seats.all()
            assign_seat = 0
            seatsAvailable = 0
            for free_seat in all_seats:
                if free_seat.available == True:
                        for passenger in passengers:
                            if passenger['seat'] == free_seat.number:
                                seatsAvailable += 1
            if(seatsAvailable == len(passengers)):
                new_booking = Booking.objects.create(
                    flight=flight,
                    price=flight.price,
                    insurance=insurance,
                    status = "PENDING",
                    start_time = datetime.now()
                )
                for passenger in passengers:
                    for free_seat in all_seats:
                        if free_seat.available == True and free_seat.number == passenger['seat']:
                            assign_seat = free_seat
                            free_seat.available = False
                            flight.number_of_seats -= 1
                            free_seat.save()
                            flight.save()
                            break
                    if(assign_seat != 0):
                        new_customer = Customer.objects.create(
                            first_name = passenger['first_name'],
                            surname = passenger['last_name'],
                            luggage = passenger['luggage'],
                            passport = passenger['passportID'],
                            seat = assign_seat,
                            booking = new_booking
                        )
                        assign_seat = 0
                    else:
                        raise Http404("Seats Unavailable")
            else:
                raise Http404("Seats Unavailable")
        except Flight.DoesNotExist:
            return JsonResponse({'error': 'Flight not found.'}, status=404) 
        new_booking.customer = new_customer
        new_booking.save()  

        booking_response = {
            "flight_id": flight.id,
            "booking_id": new_booking.id,
            "passengers": passengers,
            "priority": priority,
            "insurance": insurance,
            "status": "Waiting for payment"
        }
        return JsonResponse(booking_response, status=201)




@csrf_exempt
def delete_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        booking.delete()
        return JsonResponse({'message': 'Booking deleted successfully.'}, status=200)
    except Booking.DoesNotExist:
        return JsonResponse({'error': 'Booking not found.'}, status=404)

@csrf_exempt
def pay(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        booking.status = 'PAID'
        booking.save()
        allCust = Customer.objects.filter(booking_id=booking_id)
        custArr = []
        for customer in allCust:
            custArr.append({
                "customer_id": customer.id,
                "name": str(customer.first_name+" "+customer.surname),
                "passport_id": customer.passport,
                "seat": customer.seat.number,
                "luggage":customer.luggage
            })

        return JsonResponse({
            'booking_id': booking.id,
            "passengers": custArr,
            "priority": True,
            'insurance': booking.insurance,
            'status': "PAID"
        }, status=200)
    except Booking.DoesNotExist:
        return JsonResponse({'error': 'Booking not found.'}, status=404)

@csrf_exempt
def get_booking_details(request, booking_id):
    try:

        allCust = Customer.objects.filter(booking_id=booking_id)
        custArr = []
        for customer in allCust:
            custArr.append({
                "customer_id": customer.id,
                "name": str(customer.first_name+" "+customer.surname),
                "passport_id": customer.passport,
                "seat": customer.seat.number,
                "luggage":customer.luggage
            })


        booking = Booking.objects.get(id=booking_id)
        booking_dict = {
            'booking_id': booking.id,
            'flight_id': booking.flight.id,
            'combined_price':booking.price,
            'passengers':custArr,
            'priority':True,
            'insurnace':booking.insurance,
            'status':booking.status
        }
        return JsonResponse(booking_dict, status=200)
    except Booking.DoesNotExist:
        return JsonResponse({'error': 'Booking not found.'}, status=404)

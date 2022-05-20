from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Trip, City, Country
from .forms import TripForm, UpdateTripForm
from users.models import Passenger, Driver
from .filters import TripFilter


def add_trip(request):
    submitted = False
    userDriver = Driver.objects.filter(user=request.user)
    if len(userDriver) == 0:
        messages.success(
            request, ('You are having no registered drivers currently. Add one to proceed'))
        return redirect('add-driver')
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = TripForm(request.user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('trip-details', form.save().pk)
        else:
            form = TripForm(request.user)
        return render(request, 'trips/add_trip.html', {'form': form})
    else:
        messages.success(
            request, ('You must be authorized to add a trip'))
        return redirect('login')


def my_trips(request):
    if request.user.is_authenticated:
        tripsAsPassenger = Trip.objects.filter(
            passengers__user=request.user).order_by('start_date_and_time')
        tripsAsDriver = Trip.objects.filter(
            driver__user=request.user).order_by('start_date_and_time')
        if len(tripsAsPassenger | tripsAsDriver) > 0:
            return render(request, 'trips/my_trips.html',
                          {
                              'tripsAsPassenger': tripsAsPassenger if len(Trip.objects.filter(passengers__user=request.user)) > 0 else None,
                              'tripsAsDriver': tripsAsDriver if len(Trip.objects.filter(driver__user=request.user)) > 0 else None
                          })
        else:
            messages.success(
                request, ('Seems like you are not participating in any trip right now'))
            return render(request, 'trips/my_trips.html', {'tripsAsPassenger': None, 'tripsAsDriver': None})
    else:
        messages.success(
            request, ('You must be authorized to obtain data about your trips'))
        return redirect('login')


def trip_free_place(request, trip_id):
    if request.user.is_authenticated:
        trip = Trip.objects.get(pk=trip_id)
        if request.method == "POST":
            if request.POST.get('deleteUserPassenger'):
                trip.passengers.remove(request.POST.get('deleteUserPassenger'))
                trip.save()
                messages.success(request, ("Place was succesfully freed"))
                return redirect('my-trips')
        else:
            if len(trip.passengers.all().filter(user=request.user)) <= 0:
                messages.success(
                    request, ('You are not holding place in this trip'))
                return redirect('my-trips')
            elif len(trip.passengers.all().filter(user=request.user)) == 1:
                trip.passengers.remove(
                    trip.passengers.all().filter(user=request.user)[0])
                messages.success(request, ("Place was succesfully freed"))
                return redirect('my-trips')
            else:
                activePassengers = trip.passengers.all()
                userPassengers = Passenger.objects.filter(
                    user=request.user) & activePassengers
                return render(request, 'trips/trip_details.html', {
                    'trip': trip,
                    'passengers': activePassengers,
                    'userPassengers': userPassengers,
                    'deleteUserPassanger': True
                })
    else:
        messages.success(
            request, ('You must be authorized to free place'))
        return redirect('login')


def delete_trip(request, trip_id):
    if request.user.is_authenticated:
        trip = Trip.objects.get(pk=trip_id)
        if trip.driver.user == request.user:
            trip.delete()
            messages.success(
                request, ('Trip was sucesfully deleted'))
            return redirect('my-trips')
        else:
            messages.success(
                request, ('This trip does not belong to you!'))
            return redirect('my-trips')
    else:
        messages.success(
            request, ('You must be authorized to book a place'))
        return redirect('login')


def trip_details(request, trip_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            trip = Trip.objects.get(pk=trip_id)
            print(trip)
            activePassengers = trip.passengers.all()
            userPassengers = Passenger.objects.filter(
                user=request.user)
            userPassengers = userPassengers.exclude(id__in=activePassengers)
            if request.POST.get('userPassenger'):
                trip.passengers.add(request.POST.get('userPassenger'))
                trip.save()
                messages.success(request, ("Passeger succesfully added"))
                return render(request, 'trips/trip_details.html', {'trip': trip, 'passengers': activePassengers})
            else:
                if len(userPassengers) == 0:
                    return redirect('add-passenger', trip_id)
                else:
                    messages.success(request, ("Please, select a passenger"))
                    return render(request, 'trips/trip_details.html', {
                        'trip': trip,
                        'passengers': activePassengers,
                        'userPassengers': userPassengers,
                        'showSelection': True
                    })
        else:
            messages.success(
                request, ('You must be authorized to book a place'))
            return redirect('login')
    else:
        trip = Trip.objects.get(pk=trip_id)
        print(trip.passengers.all())
        activePassengers = trip.passengers.all()
        return render(request, 'trips/trip_details.html', {'trip': trip, 'passengers': activePassengers})


def active_trips(request):
    trips = Trip.objects.filter(
        start_date_and_time__gte=timezone.now()).order_by('start_date_and_time')
    tripFilter = TripFilter(request.GET, queryset=trips)
    trips = tripFilter.qs
    paginator = Paginator(trips, 2)
    page = request.GET.get('page')
    tripsForPage = paginator.get_page(page)
    if request.GET.get('showFilter') == 'Filter':
        return render(request, 'trips/active_trips.html', {'trips': trips, 'filter': tripFilter, 'tripsForPage': tripsForPage, 'showFilter': True})
    return render(request, 'trips/active_trips.html', {'trips': trips, 'filter': tripFilter, 'tripsForPage': tripsForPage})


def update_trip(request, trip_id):
    if request.user.is_authenticated:
        trip = Trip.objects.get(pk=trip_id)
        if request.method == 'POST':
            form = UpdateTripForm(request.user, request.POST, instance=trip)
            if form.is_valid():
                form.save()
                return redirect('trip-details', trip_id)
        else:
            form = UpdateTripForm(request.user, instance=trip)
        return render(request, 'trips/update_trip.html', {'trip': trip, 'form': form})
    else:
        messages.success(
            request, ('You must be authorized to update a trip'))
        return redirect('login')


def home(request):
    return render(request, 'trips/home.html', {})


def load_cities(request):
    country_id = request.GET.get('country_id')
    if country_id == '':
        cities = City.objects.none()
        return render(request, 'trips/city_ddl.html', {'cities': cities})
    else:
        cities = City.objects.filter(country_id=country_id)
        return render(request, 'trips/city_ddl.html', {'cities': cities})

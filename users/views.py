from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm, DriverCreationForm, PassengerCreationForm
from .models import Driver, Passenger
from trips.models import Trip


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, ('Such user does not exist.'))
            return redirect('login')
    else:
        return render(request, 'auth/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ('You were log out.'))
    return redirect('home')


def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ('Registration successful.'))
            return redirect('home')
    else:
        form = RegisterUserForm
    return render(request, 'auth/register.html', {'form': form, })


def add_driver(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = DriverCreationForm(request.POST)
            if form.is_valid():
                form.save()
                driverPK = form.save().id
                driver = Driver.objects.get(id=driverPK)
                driver.user = request.user
                driver.save()
                messages.success(request, ('Driver was added successfully.'))
                return redirect('add-trip')
        else:
            form = DriverCreationForm
        return render(request, 'auth/add_driver.html', {'form': form})
    else:
        messages.success(
            request, ('You must be authorized to add a driver'))
        return redirect('login')


def add_passenger(request, trip_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PassengerCreationForm(request.POST)
            if form.is_valid():
                form.save()
                passengerPK = form.save().id
                passenger = Passenger.objects.get(id=passengerPK)
                passenger.user = request.user
                passenger.save()
                trip = Trip.objects.get(pk=trip_id)
                trip.passengers.add(passenger)
                trip.save()
                messages.success(
                    request, ('Passenger was added successfully.'))
                return redirect('trip-details', trip_id)
        else:
            form = PassengerCreationForm
        return render(request, 'auth/add_passenger.html', {'form': form, 'trip_id': trip_id})
    else:
        messages.success(
            request, ('You must be authorized to add a driver'))
        return redirect('login')

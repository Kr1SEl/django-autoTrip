from django import forms
from django.utils import timezone
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import Trip, City, Country
from users.models import Driver, Passenger
from bootstrap_datepicker_plus.widgets import DateTimePickerInput


class TripForm(ModelForm):
    class Meta:
        model = Trip
        fields = ('driver', 'start_country', 'start_city', 'end_country', 'end_city',
                  'num_of_places', 'start_date_and_time',
                  'description',)
        labels = {
            'num_of_places': '',
            'start_date_and_time': '',
            'description': '',
            'start_country': 'From:',
            'start_city': '',
            'end_country': 'To:',
            'end_city': '',
            'driver': 'Driver'
        }
        widgets = {
            'num_of_places': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number Of Places'}),
            'start_date_and_time': DateTimePickerInput(attrs={'placeholder': 'Department Time'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }

    def __init__(self, user, *args, **kwargs):
        super(TripForm, self).__init__(*args, **kwargs)
        self.fields['start_country'].widget.attrs['class'] = 'form-control'
        self.fields['start_city'].widget.attrs['class'] = 'form-control'
        self.fields['end_country'].widget.attrs['class'] = 'form-control'
        self.fields['end_city'].widget.attrs['class'] = 'form-control'
        self.fields['driver'].widget.attrs['class'] = 'form-control'
        self.fields['start_city'].queryset = City.objects.none()
        self.fields['end_city'].queryset = City.objects.none()
        self.fields['driver'].queryset = Driver.objects.filter(
            user=user)

        if 'start_country' in self.data:
            try:
                country_id = int(self.data.get('start_country'))
                self.fields['start_city'].queryset = City.objects.filter(
                    country_id=country_id).order_by('city_name')
            except (ValueError, TypeError):
                pass
        if 'end_country' in self.data:
            try:
                country_id = int(self.data.get('end_country'))
                self.fields['end_city'].queryset = City.objects.filter(
                    country_id=country_id).order_by('city_name')
            except (ValueError, TypeError):
                pass

    def clean(self):
        cleaned_data = super().clean()
        time = cleaned_data.get('start_date_and_time')
        if time < timezone.now():
            raise ValidationError(
                'Start time must be grater than current time')
        start_city = cleaned_data.get('start_city')
        end_city = cleaned_data.get('end_city')
        if start_city == end_city:
            raise ValidationError(
                'Start city and end city must be different')
        return cleaned_data


class UpdateTripForm(ModelForm):
    class Meta:
        model = Trip
        fields = ('driver', 'start_date_and_time',
                  'description', )
        labels = {
            'start_date_and_time': '',
            'description': '',
            'driver': 'Driver'
        }
        widgets = {
            'start_date_and_time': DateTimePickerInput(attrs={'placeholder': 'Department Time'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }

    def __init__(self, user, *args, **kwargs):
        super(UpdateTripForm, self).__init__(*args, **kwargs)
        self.fields['driver'].widget.attrs['class'] = 'form-control'
        self.fields['driver'].queryset = Driver.objects.filter(
            user=user)

    def clean(self):
        cleaned_data = super().clean()
        time = cleaned_data.get("start_date_and_time")
        if time < timezone.now():
            raise ValidationError(
                "Start time must be grater than current time")
        return cleaned_data

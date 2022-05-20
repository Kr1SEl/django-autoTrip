from .models import Trip, City, Country
from django.db import models
from django import forms
from django_filters import DateTimeFilter, CharFilter
import django_filters
from bootstrap_datepicker_plus.widgets import DateTimePickerInput


class TripFilter(django_filters.FilterSet):
    start_date_and_time = DateTimeFilter(
        field_name="start_date_and_time", lookup_expr='gte', label='', widget=DateTimePickerInput(attrs={'placeholder': 'Departure Time'}))

    class Meta:
        model = Trip
        fields = ('start_date_and_time', 'start_country',
                  'start_city', 'end_country',
                  'end_city')

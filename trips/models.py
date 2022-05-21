from django.db import models
from django.db.models import Q
from users.models import Passenger, Driver
from django.utils import timezone


class Country(models.Model):
    country_name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.country_name}'

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'


class City(models.Model):
    city_name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.city_name}'

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'


class Trip(models.Model):
    num_of_places = models.PositiveIntegerField()
    start_date_and_time = models.DateTimeField()
    places_left = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True)
    passengers = models.ManyToManyField(Passenger, blank=True)
    start_country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name='Start_country')
    end_country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name='End_country')
    start_city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name='Start_city')
    end_city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name='End_city')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)

    @property
    def hasDescription(self):
        return self.description != ''

    @property
    def isActive(self):
        return timezone.now() > self.start_date_and_time

    def __str__(self):
        return f'Start City: {self.start_city} | End City: {self.end_city} | {self.driver}'

from django.db import models
from django.contrib.auth.models import User


class Base(models.Model):
    id = models.AutoField(primary_key=True)

    class Meta:
        abstract = True


class Profile(Base):
    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_CHOICES = [(GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female')]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    gender = models.IntegerField(choices=GENDER_CHOICES)
    with_music = models.BooleanField()
    smoking = models.BooleanField()
    sociable = models.BooleanField()

    class Meta:
        abstract = True


class Passenger(Profile):
    with_bagage = models.BooleanField()
    with_animals = models.BooleanField()
    with_child = models.BooleanField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return (f'{self.first_name} {self.last_name}, {self.age} yo |'
                f"{' Loves music |' if self.with_music else ''}"
                f"{' Smoking |' if self.smoking else ''}"
                f"{' Communicative |' if self.sociable else ''}"
                f"{' Has bagage |' if self.with_bagage else ''}"
                f"{' With animal |' if self.with_animals else ''}"
                f"{' With child' if self.with_child else ''}")


class Driver(Profile):
    experience_in_driving = models.PositiveIntegerField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}, {self.age} yo, Driving experience: {self.experience_in_driving}'

from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Driver, Passenger


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


class DriverCreationForm(ModelForm):
    first_name = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    age = forms.DecimalField(max_value=120, min_value=12, widget=forms.NumberInput(
        attrs={'class': 'form-control'}))
    experience_in_driving = forms.DecimalField(max_value=100, min_value=1, widget=forms.NumberInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = Driver
        fields = ('first_name', 'last_name', 'age',
                  'experience_in_driving', 'gender',
                  'with_music', 'smoking', 'sociable')

    def __init__(self, *args, **kwargs):
        super(DriverCreationForm, self).__init__(*args, **kwargs)
        self.fields['with_music'].widget.attrs['class'] = 'form-check-input'
        self.fields['smoking'].widget.attrs['class'] = 'form-check-input'
        self.fields['sociable'].widget.attrs['class'] = 'form-check-input'
        self.fields['gender'].widget.attrs['class'] = 'form-select'


class PassengerCreationForm(ModelForm):
    first_name = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    age = forms.DecimalField(max_value=120, min_value=12, widget=forms.NumberInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = Passenger
        fields = ('first_name', 'last_name', 'age',
                  'gender', 'with_music', 'smoking',
                  'sociable', 'with_bagage', 'with_animals',
                  'with_child')
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(PassengerCreationForm, self).__init__(*args, **kwargs)
        self.fields['with_music'].widget.attrs['class'] = 'form-check-input'
        self.fields['smoking'].widget.attrs['class'] = 'form-check-input'
        self.fields['sociable'].widget.attrs['class'] = 'form-check-input'
        self.fields['with_bagage'].widget.attrs['class'] = 'form-check-input'
        self.fields['with_animals'].widget.attrs['class'] = 'form-check-input'
        self.fields['with_child'].widget.attrs['class'] = 'form-check-input'
        self.fields['gender'].widget.attrs['class'] = 'form-select'

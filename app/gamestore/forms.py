from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from gamestore.models import Game
from datetime import date


class UserForm(UserCreationForm):
    birthDate = forms.DateField(help_text='Required. Format: MM/DD/YYYY')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'birthDate',  'password1', 'password2',)
    
    def clean_first_name(self):
        return self.cleaned_data['first_name']
    
    def clean_last_name(self):
        return self.cleaned_data['last_name']

    def clean_username(self):
        username = self.cleaned_data['username']
        self.check_user_uniqueness(error="User with this username already exists.", username=username)
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        self.check_user_uniqueness(error="User with this email already exists.", email=email)
        return email

    def clean_birthDate(self):
        birthDate = self.cleaned_data['birthDate']
        currentDate = date.today()
        if birthDate > currentDate:
            raise forms.ValidationError("Birth date is greater than current date.")
        return birthDate

    def clean_age(self):
        age = self.calculate_age(self.cleaned_data['birthDate'])
        if age > 120:
            raise forms.ValidationError('You are overage (>120).')
        if age < 14:
            raise forms.ValidationError('You are underage (<14).')
        return age

    def calculate_age(self, birthDate):
        today = date.today()
        return today.year - birthDate.year - ((today.month, today.day)
               < (birthDate.month, birthDate.day))

    def check_user_uniqueness(self, error, **field):
        another_user = User.objects.filter(**field)
        if another_user:
            raise forms.ValidationError(error)

class GameForm(ModelForm):

    class Meta:
        model = Game
        fields = ('name', 'price', 'category', 'pictureUrl', 'description', 'gameUrl', 'age_restriction',)


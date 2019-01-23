from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
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

    def clean_email(self):
        email = self.check_email_uniqueness()
        return email

    def check_email_uniqueness(self):
        email = self.cleaned_data['email']
        another_email = User.objects.filter(email=email)
        if another_email:
            raise forms.ValidationError("A user with that email already exists.")
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
            error = 'You are overage (>120).'
            self.add_error('birthDate', error)
            raise forms.ValidationError(error)
        if age < 14:
            error = 'You are underage (<14).'
            self.add_error('birthDate', error)
            raise forms.ValidationError(error)
        return age

    def calculate_age(self, birthDate):
        today = date.today()
        return today.year - birthDate.year - ((today.month, today.day)
               < (birthDate.month, birthDate.day))

class GameForm(ModelForm):

    class Meta:
        model = Game
        fields = ('name', 'price', 'category', 'pictureUrl', 'description', 'gameUrl', 'age_limit',)

    def clean(self):
        cleaned_data = self.cleaned_data
        cleaned_data['price'] = self.clean_price()
        cleaned_data['age_limit'] = self.clean_age_limit()
        return cleaned_data

    def clean_price(self):
        price = self.cleaned_data['price']
        if price > 10000:
            raise forms.ValidationError("Sorry, we don't allow prices more than 10000 UER")
        if price < 0:
            raise forms.ValidationError("Price have to be positive number")
        return round(price, 2)

    def clean_age_limit(self):
        age_limit = self.cleaned_data['age_limit']
        if age_limit > 120:
            raise forms.ValidationError("Please, enter age limit less than 120")
        if age_limit < 3:
            raise forms.ValidationError("Please, enter age limit greater than 3")
        return age_limit
        
class UserUpdateForm(UserChangeForm):
    birthDate = forms.DateField(help_text='Required. Format: MM/DD/YYYY')
    gender = forms.CharField() #Choice form?
    
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name', 
            'username', 
            'email', 
            'birthDate',
            'gender',
            'password'
        )

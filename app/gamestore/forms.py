from django import forms
from django.forms import Form
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from gamestore.models import Game
from datetime import date

def check_user_uniqueness(error, **field):
    another_user = User.objects.filter(**field)
    if another_user:
        raise forms.ValidationError(error)
        
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
        check_user_uniqueness(error="User with this username already exists.", username=username)
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        check_user_uniqueness(error="User with this email already exists.", email=email)
        return email
        
    def clean_birthDate(self):
        birthDate = self.cleaned_data['birthDate']
        currentDate = date.today()
        if birthDate > currentDate:
            raise forms.ValidationError("Birth date is greater than current date.")
        return birthDate
        
    
class GameForm(Form):
    
    class Meta:
        model = Game
        fields = ('name',)
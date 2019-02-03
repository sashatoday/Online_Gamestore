from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from gamestore.models import Game
from datetime import date
from dateutil.relativedelta import relativedelta
from gamestore.core.constants import *


def calculate_age(birth_date):
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day)
           < (birth_date.month, birth_date.day))

def birth_date_is_valid(birth_date):
    age = calculate_age(birth_date)
    if age > 120:
        raise forms.ValidationError("You are overage (>120).")
    if age < 14:
        raise forms.ValidationError("You are underage (<14).")

def check_price(price):
    if price > 10000:
        raise forms.ValidationError("Sorry, we don't allow prices more than 10000 UER")
    if price < 0:
        raise forms.ValidationError("Price have to be positive number")
    return round(price, 2)

def check_age_limit(age_limit):
    if age_limit > 120:
        raise forms.ValidationError("Please, enter age limit less than 120")
    if age_limit < 3:
        raise forms.ValidationError("Please, enter age limit greater than 3")
    return age_limit

class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'birthDate',
            'gender', 
            'password1',
            'password2',
        )
    username = forms.CharField(
        help_text = 'Remember: You will be not able to change your username in future',
        required = True,
        widget   = forms.TextInput(attrs = {'class' : 'form-control here', 'maxlength' : 50})
    )
    first_name = forms.CharField(
        required = True,
        widget   = forms.TextInput(attrs = {'class' : 'form-control here', 'maxlength' : 50})
    )
    last_name = forms.CharField(
        required = True,
        widget   = forms.TextInput(attrs = {'class' : 'form-control here', 'maxlength' : 50})
    )
    email = forms.CharField(
        required = True,
        widget   = forms.TextInput(attrs= {'class' : 'form-control here', 'type' : 'email', 'maxlength' : 50, 'placeholder': 'you@example.com'})
    )
    birthDate = forms.DateField(
        help_text = 'Your age should be more than 14 and less than 120',
        label     = 'Birth date',
        required  = True,
        widget    = forms.DateInput(attrs = {'type' : 'date', 'class' : 'form-control here', 'min': date.today() + relativedelta(years=-120), 'max' : date.today() + relativedelta(years=-14)})
    )
    gender = forms.ChoiceField(
        choices  = GENDER_CHOICES,
        label    = 'Gender',
        required = True,
        widget   = forms.Select(attrs = {'class' : 'form-control here', 'maxlength' : 1})
    )
    password1 = forms.CharField(
        label  = "Password",
        required = True,
        widget = forms.PasswordInput(attrs= {'class' : 'form-control here', 'maxlength' : 50})
    )

    password2 = forms.CharField(
        label  = "Repeat password",
        required = True,
        widget = forms.PasswordInput(attrs= {'class' : 'form-control here', 'maxlength' : 50})
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        another_email = User.objects.filter(email=email)
        if another_email:
            raise forms.ValidationError("A user with that email already exists.")
        return email

    def clean_birthDate(self):
        birth_date = self.cleaned_data['birthDate']
        birth_date_is_valid(birth_date)
        return birth_date

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )
    username = forms.CharField(
        required = True,
        widget   = forms.TextInput(attrs = {'class' : 'form-control here', 'readonly' : 'readonly'})
    )
    first_name = forms.CharField(
        required = True,
        widget   = forms.TextInput(attrs = {'class' : 'form-control here'})
    )
    last_name = forms.CharField(
        required = True,
        widget   = forms.TextInput(attrs = {'class' : 'form-control here'})
    )
    email = forms.CharField(
        required = True,
        widget   = forms.TextInput(attrs= {'class' : 'form-control here', 'type' : 'email'})
    )
    def clean_email(self):
        email = self.cleaned_data['email']
        users = User.objects.exclude(username=self.cleaned_data['username'])
        another_email = users.filter(email=email)
        if another_email:
            raise forms.ValidationError("A user with that email already exists.")
        return email

class UserProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'gender',
            'birthDate',
            'country',
            'city',
            'address',
            'photoUrl',
            'role',
            'bio',
        )
    gender = forms.ChoiceField(
        choices  = GENDER_CHOICES, 
        label    = 'Gender',
        required = True,
        widget   = forms.Select(attrs = {'class' : 'form-control here', 'maxlength' : 1})
    )
    country = forms.CharField(
        label    = 'Country',
        required = False,
        widget   = forms.TextInput(attrs = {'class' : 'form-control here', 'maxlength' : 20})
    )
    city = forms.CharField(
        label    = 'City',
        required = False,
        widget   = forms.TextInput(attrs = {'class' : 'form-control here', 'maxlength' : 30})
    )
    address = forms.CharField(
        label    = 'Address',
        required = False,
        widget   = forms.TextInput(attrs = {'class' : 'form-control here', 'maxlength' : 100})
    )
    photoUrl = forms.URLField(
        label    = 'Photo URL',
        required = False,
        widget   = forms.URLInput(attrs = {'class' : 'form-control here', 'placeholder': 'http://', 'maxlength' : 200})
    )
    role = forms.ChoiceField(
        choices  = ROLE_CHOICES, 
        label    = 'Role',
        required = True,
        widget   = forms.Select(attrs = {'class' : 'form-control here', 'maxlength' : 1})
    )
    birthDate = forms.DateField(
        help_text = 'Your age should be more than 14 and less than 120',
        label     = 'Birth date',
        required  = True,
        widget    = forms.DateInput(attrs = {'type' : 'date', 'class' : 'form-control here', 'min': date.today() + relativedelta(years=-120), 'max' : date.today() + relativedelta(years=-14)})
    )
    bio = forms.CharField(
        label    = 'Bio',
        required = False,
        widget   = forms.Textarea(attrs= {'class' : 'form-control here', 'maxlength' : 200})
    )

    def clean_birthDate(self):
        birthDate = self.cleaned_data['birthDate']
        birth_date_is_valid(birthDate)
        return birthDate

class ChangePasswordForm(PasswordChangeForm):

    old_password = forms.CharField(
        label  = "Old password", 
        widget = forms.PasswordInput(attrs= {'class' : 'form-control here'})
    )
    new_password1 = forms.CharField(
        label  = "New password",
        widget = forms.PasswordInput(attrs= {'class' : 'form-control here'})
    )
    new_password2 = forms.CharField(
        label  = "Confirm new password",
        widget = forms.PasswordInput(attrs= {'class' : 'form-control here'})
    )

class GameForm(ModelForm):

    class Meta:
        model = Game
        fields = (
            'name',
            'price',
            'category',
            'pictureUrl',
            'description',
            'gameUrl',
            'age_limit',
        )
    name = forms.CharField(
        label  = "Title",
        required = True,
        widget = forms.TextInput(attrs= {'class' : 'form-control here', 'maxlength' : 50})
    )
    price = forms.FloatField(
        label  = "Price in EUR",
        required = True,
        widget = forms.NumberInput(attrs= {'class' : 'form-control here', 'placeholder': "0.00", 'min' : 0, 'max' : 10000, 'size' : 0.01})
    )
    pictureUrl = forms.URLField(
        label  = "Picture URL",
        required = False,
        widget = forms.URLInput(attrs= {'class' : 'form-control here', 'maxlength' : 200, 'placeholder': 'http://'})
    )
    description = forms.CharField(
        label  = "Description",
        required = False,
        widget = forms.Textarea(attrs= {'class' : 'form-control here', 'maxlength' : 200})
    )
    gameUrl = forms.URLField(
        label  = "Game URL",
        required = True,
        widget = forms.URLInput(attrs= {'class' : 'form-control here', 'maxlength' : 200, 'placeholder': 'http://'})
    )
    category = forms.ChoiceField(
        choices  = CATEGORY_CHOICES,
        label    = 'Category',
        required = True,
        widget   = forms.Select(attrs = {'class' : 'form-control here', 'maxlength' : 20})
    )
    age_limit = forms.IntegerField(
        help_text = 'Indicate age limit for users. You can enter number between 3 and 120',
        label  = "Age limit",
        required = True,
        widget = forms.NumberInput(attrs= {'class' : 'form-control here', 'min' : 3, 'max' : 120, 'size' : 1})
    )

    def clean(self):
        cleaned_data = self.cleaned_data
        cleaned_data['price'] = check_price(self.cleaned_data['price'])
        cleaned_data['age_limit'] = check_age_limit(self.cleaned_data['age_limit'])
        return cleaned_data


class GameUpdateForm(ModelForm):

    class Meta:
        model = Game
        fields = (
            'name',
            'price',
            'category',
            'pictureUrl',
            'description',
            'gameUrl',
            'age_limit',
        )
    name = forms.CharField(
        label  = "Title",
        required = True,
        widget = forms.TextInput(attrs= {'class' : 'form-control here', 'maxlength' : 50, 'readonly' : 'readonly'})
    )
    price = forms.FloatField(
        label  = "Price in EUR",
        required = True,
        widget = forms.NumberInput(attrs= {'class' : 'form-control here', 'placeholder': "0.00", 'min' : 0, 'max' : 10000, 'size' : 0.01})
    )
    pictureUrl = forms.URLField(
        label  = "Picture URL",
        required = False,
        widget = forms.URLInput(attrs= {'class' : 'form-control here', 'maxlength' : 200, 'placeholder': 'http://'})
    )
    description = forms.CharField(
        label  = "Description",
        required = False,
        widget = forms.Textarea(attrs= {'class' : 'form-control here', 'maxlength' : 200})
    )
    gameUrl = forms.URLField(
        label  = "Game URL",
        required = True,
        widget = forms.URLInput(attrs= {'class' : 'form-control here', 'maxlength' : 200, 'placeholder': 'http://'})
    )
    category = forms.ChoiceField(
        choices  = CATEGORY_CHOICES,
        label    = 'Category',
        required = True,
        widget   = forms.Select(attrs = {'class' : 'form-control here', 'maxlength' : 20})
    )
    age_limit = forms.IntegerField(
        help_text = 'Indicate age limit for users. You can enter number between 3 and 120',
        label  = "Age limit",
        required = True,
        widget = forms.NumberInput(attrs= {'class' : 'form-control here', 'min' : 3, 'max' : 120, 'size' : 1})
    )

    def clean(self):
        cleaned_data = self.cleaned_data
        cleaned_data['price'] = check_price(self.cleaned_data['price'])
        cleaned_data['age_limit'] = check_age_limit(self.cleaned_data['age_limit'])
        return cleaned_data

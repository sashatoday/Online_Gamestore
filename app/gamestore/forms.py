from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from gamestore.models import Game
from datetime import date

MALE = 'M'
FEMALE = 'F'
UNKNOWN = 'U'
ADMIN = 'A'
DEVELOPER = 'D'
PLAYER = 'P'
GENDER_CHOICES = (
    (MALE, 'Male'),
    (FEMALE, 'Female'),
    (UNKNOWN, 'Unknown'),
)
ROLE_CHOICES = (
    (ADMIN, 'Admin'),
    (DEVELOPER, 'Developer'),
    (PLAYER, 'Player'),
)

def email_is_unique(email):
    another_email = User.objects.filter(email=email)
    if another_email:
        return False
    return True

def birth_date_is_valid(birth_date):
    currentDate = date.today()
    if birth_date > currentDate:
        return False
    return True

class UserForm(UserCreationForm):

    birthDate = forms.DateField(help_text='Required. Format: MM/DD/YYYY')
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES, 
        required=True,
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'birthDate',
            'gender', 
            'password1',
            'password2',
        )

    def clean_first_name(self):
        return self.cleaned_data['first_name']
    
    def clean_last_name(self):
        return self.cleaned_data['last_name']

    def clean_email(self):
        email = self.check_email_uniqueness()
        return email

    def clean_gender(self):
        return self.cleaned_data['gender']

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

class UserUpdateForm(forms.ModelForm):

    username = forms.CharField(
        required = True,
        widget   = forms.TextInput(attrs = {'class' : 'form-control here'})
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

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name', 
            'email', 
        )

    '''
    def clean_email(self):
        email = self.cleaned_data['email']
        if not email_is_unique(email):
            raise forms.ValidationError("A user with that email already exists.")
        return email
    '''

class UserProfileUpdateForm(forms.ModelForm):

    gender = forms.ChoiceField(
        choices  = GENDER_CHOICES, 
        label    = 'Gender',
        required = False,
        widget   = forms.Select(attrs = {'class' : 'form-control here'})
    )

    country = forms.CharField(
        label    = 'Country',
        required = False,
        widget   = forms.TextInput(attrs = {'class' : 'form-control here'})
    )

    city = forms.CharField(
        label    = 'City',
        required = False,
        widget   = forms.TextInput(attrs = {'class' : 'form-control here'})
    )

    address = forms.CharField(
        label    = 'Address',
        required = False,
        widget   = forms.TextInput(attrs = {'class' : 'form-control here'})
    )
 
    photoUrl = forms.URLField(
        label    = 'Photo URL',
        initial  = 'http://',
        required = False,
        widget   = forms.URLInput(attrs = {'class' : 'form-control here'})
    )

    role = forms.ChoiceField(
        choices  = ROLE_CHOICES, 
        label    = 'Role',
        required = True,
        widget   = forms.Select(attrs = {'class' : 'form-control here'})
    )

    birthDate = forms.DateField(
        help_text = 'Required. Format: MM/DD/YYYY',
        label     = 'Birth date',
        required  = False,
        widget    = forms.DateInput(attrs = {'type' : 'date', 'class' : 'form-control here', 'min': '1899-01-01', 'max' : date.today()})
    )

    bio = forms.CharField(
        label    = 'Bio',
        required = False,
        widget   = forms.Textarea(attrs= {'class' : 'form-control here'})
    )
    
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

    def clean_birthDate(self):
        birthDate = self.cleaned_data['birthDate']
        if not birth_date_is_valid(birthDate):
            raise forms.ValidationError("Birth date is greater than current date.")
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
import datetime
from django.test import TestCase
from django.utils import timezone
import copy
from gamestore.forms import UserForm
from django.contrib.auth.models import User
from gamestore.models import UserProfile


valid_date = datetime.date(1990, 11, 23)
form_data = {"username": "testuser",
            "first_name": "Bacha",
            "last_name": "Debela",
            "email": "bacha@gmail.com",
            "birth_date": valid_date,
            "gender": "M",
            "password1": "TestPassword1!",
            "password2": "TestPassword1!",
            "check_agreement": "on"}
class UserFormTest(TestCase): 
    fixtures = ['gamestore.json']
    
    def _assert_invalid_form(self, data):
        invalid_form = UserForm(data=data)
        self.assertFalse(invalid_form.is_valid())

    def test_user_profile_field_help_texts(self):
        form = UserForm()
        self.assertEqual(form.fields["username"].help_text, "Remember: You will be not able to change your username in future")
        self.assertEqual(form.fields["birth_date"].help_text, "Your age should be more than 14 and less than 120")
    
    def test_user_form_username_is_not_empty(self):
        data = copy.deepcopy(form_data)
        data["username"] = ""
        self._assert_invalid_form(data)
    
    def test_user_form_first_name_is_not_empty(self):
        data = copy.deepcopy(form_data)
        data["first_name"] = ""
        self._assert_invalid_form(data)

    def test_user_form_last_name_is_not_empty(self):
        data = copy.deepcopy(form_data)
        data["last_name"] = ""
        self._assert_invalid_form(data)

    def test_user_form_email_is_not_empty(self):
        data = copy.deepcopy(form_data)
        data["email"] = ""
        self._assert_invalid_form(data)

    def test_user_form_birth_date_is_not_empty(self):
        data = copy.deepcopy(form_data)
        data["birth_date"] = ""
        self._assert_invalid_form(data)

    def test_user_form_gender_is_not_empty(self):
        data = copy.deepcopy(form_data)
        data["gender"] = ""
        self._assert_invalid_form(data)

    def test_user_form_password_is_not_empty(self):
        data = copy.deepcopy(form_data)
        data["password1"] = ""
        self._assert_invalid_form(data)

    def test_user_form_check_agreement_is_not_empty(self):
        data = copy.deepcopy(form_data)
        data["check_agreement"] = ""
        self._assert_invalid_form(data)
    
    def test_user_form_email_is_unique(self):
        data = copy.deepcopy(form_data)
        data["email"] = "alice@gmail.com"
        self._assert_invalid_form(data)

    def test_user_form_birth_date_valid_age(self):
        valid_form = UserForm(data=form_data)
        self.assertTrue(valid_form.is_valid())
    
    def test_user_form_birth_date_min_age(self):
        invalid_date = datetime.date.today()
        data = copy.deepcopy(form_data)
        data["birth_date"] = invalid_date
        self._assert_invalid_form(data)
    
    def test_user_form_birth_date_max_age(self):
        invalid_date = datetime.date(1890, 11, 23)
        data = copy.deepcopy(form_data)
        data["birth_date"] = invalid_date
        self._assert_invalid_form(data)


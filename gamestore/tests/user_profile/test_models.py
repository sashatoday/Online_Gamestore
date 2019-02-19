from datetime import date
from django.db import models
from django.test import TestCase
from django.contrib.auth.models import User
from gamestore.models import UserProfile

class UserProfileModelTest(TestCase):
    fixtures = ['gamestore.json']
    def _testfieldtype(self, model, modelname, fieldname, type):
        try:
            field = model._meta.get_field(fieldname)
            self.assertTrue(isinstance(field, type), "Testing the type of %s field in model %s"%(fieldname, modelname))
        except FieldDoesNotExist:
            self.assertTrue(False, "Testing if field %s exists in model %s"%(fieldname, modelname))
        return field

    def testFieldTypes(self):
        self._testfieldtype(UserProfile, 'UserProfile', 'birth_date', models.DateField)
        self._testfieldtype(UserProfile, 'UserProfile', 'gender', models.CharField)
        self._testfieldtype(UserProfile, 'UserProfile', 'country', models.CharField)
        self._testfieldtype(UserProfile, 'UserProfile', 'city', models.CharField)
        self._testfieldtype(UserProfile, 'UserProfile', 'address', models.CharField)
        self._testfieldtype(UserProfile, 'UserProfile', 'bio', models.TextField)
        self._testfieldtype(UserProfile, 'UserProfile', 'photo_url', models.URLField)
        self._testfieldtype(UserProfile, 'UserProfile', 'role', models.CharField)

    def test_field_values(self):
        user_profile = UserProfile.objects.get(id=4)
        self.assertEquals(user_profile.user.username, 'test_user')
        self.assertEquals(user_profile.user.first_name, 'Alice')
        self.assertEquals(user_profile.user.last_name, 'Bob')
        self.assertEquals(user_profile.user.email, 'alice@gmail.com')
        self.assertEquals(user_profile.user.is_active, True)
        self.assertEquals(user_profile.birth_date, date(1949, 11, 11))
        self.assertEquals(user_profile.gender, 'F')
        self.assertEquals(user_profile.country, 'Finland')
        self.assertEquals(user_profile.city, 'Helsinki')
        self.assertEquals(user_profile.address, 'Antinkatu 1')
        self.assertEquals(user_profile.bio, 'Hey im alice. i like to play online game')
        self.assertEquals(user_profile.photo_url, 'http://brickingaround.com/wp-content/uploads/2017/10/sophia-cu-with-chat.png')
        self.assertEquals(user_profile.role, 'D')

    def test_object_is_developer(self):
        user_profile = UserProfile.objects.get(id=4)
        self.assertEquals(user_profile.is_developer(), True)

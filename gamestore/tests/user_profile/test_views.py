import uuid
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from gamestore.models import UserProfile

class UserAccountTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='test_user', 
                                    first_name='Alice', 
                                    last_name='Bob', 
                                    email='alice@gmail.com', 
                                    is_active=True)
        UserProfile.objects.create(user=user, 
                                    birth_date='1949-11-11', 
                                    gender='F', 
                                    country='Finland', 
                                    city='Helsinki', 
                                    address='Antinkatu 1', 
                                    bio='Hey im alice. i like to play online game', 
                                    photo_url='http://brickingaround.com/wp-content/uploads/2017/10/sophia-cu-with-chat.png', 
                                    role='D')
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('profile'))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/?next=/profile/'))

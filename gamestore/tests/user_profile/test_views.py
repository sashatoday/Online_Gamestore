import uuid
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from gamestore.models import UserProfile
from gamestore.tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

class UserAccountTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user', 
                                    first_name='Alice', 
                                    last_name='Bob', 
                                    email='alice@gmail.com',
                                    is_active=True)
        UserProfile.objects.create(user=self.user, 
                                    birth_date='1949-11-11', 
                                    gender='F', 
                                    country='Finland', 
                                    city='Helsinki', 
                                    address='Antinkatu 1', 
                                    bio='Hey im alice. i like to play online game', 
                                    photo_url='http://brickingaround.com/wp-content/uploads/2017/10/sophia-cu-with-chat.png', 
                                    role='D')
        self.user.set_password('12345')
        self.user.save()

    ### Redirecting ###
    def test_login_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('profile'))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/?next=/profile/'))

    def test_restore_account_redirect_if_logged_in(self):
        user_login = self.client.login(username="test_user", password="12345")
        self.assertTrue(user_login)
        response = self.client.get("/restore_account/")
        self.assertRedirects(response, '/search_game/')

    ### test reset_password ###
    def test_reset_password_if_not_logged_in(self):
        response = self.client.get("/reset_password/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/reset_password.html")
        self.assertTemplateUsed(response, "base.html")

    def test_reset_password_if_logged_in(self):
        user_login = self.client.login(username="test_user", password="12345")
        self.assertTrue(user_login)
        response = self.client.get("/reset_password/")
        self.assertRedirects(response, '/profile/')

    def test_reset_password_with_valid_email(self):
        response = self.client.post("/reset_password/", {'email': 'test@test.com'})
        self.assertTrue(response.context['message'])

    def test_reset_password_with_invalid_email(self):
        response = self.client.post("/reset_password/", {'email': ''})
        with self.assertRaises(KeyError):
            response.context['message']

    ### test signup (get and post) ###
    def test_signup_if_not_logged_in(self):
        response = self.client.get("/signup/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/signup.html")
        self.assertTemplateUsed(response, "base.html")

    def test_signup_if_logged_in(self):
        user_login = self.client.login(username="test_user", password="12345")
        self.assertTrue(user_login)
        response = self.client.get("/login/")
        self.assertRedirects(response, '/search_game/')

    def test_signup_with_correct_credintials(self):
        response = self.client.post("/signup/", {
            "username": "testuser",
            "first_name": "Bacha",
            "last_name": "Debela",
            "email": "bacha@gmail.com",
            "birth_date": "1999-01-01",
            "gender": "M",
            "password1": "TestPassword1!",
            "password2": "TestPassword1!",
            "check_agreement": "on"}, follow=True)
        self.assertRedirects(response, '/signup/thanks/')

    def test_signup_with_incorrect_credintials(self):
        response = self.client.post("/signup/", {
            "username": "testuser",
            "first_name": -1,
            "last_name": "Debela",
            "email": "bacha@gmail.com",
            "birth_date": "1999-01",
            "gender": 3,
            "password1": "TestPassw",
            "password2": "TestPassword1!",
            "check_agreement": "o"}, follow=True)
        self.assertTrue(response.context['form'].errors)

    ### login views (get and post) ###
    def test_login_if_not_logged_in(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/login.html")
        self.assertTemplateUsed(response, "base.html")

    def test_login_if_logged_in(self):
        user_login = self.client.login(username="test_user", password="12345")
        self.assertTrue(user_login)
        response = self.client.get("/login/")
        self.assertRedirects(response, '/search_game/')
    
    def test_login_with_wrong_credintials(self):
        response = self.client.post("/login/", {'username': 'test_user', 'password': '1234'}, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)
    
    def test_login_with_correct_credintials(self):
        response = self.client.post("/login/", {'username': 'test_user', 'password': '12345'}, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    ### test logout ###
    def test_logout(self):
        user_login = self.client.login(username="test_user", password="12345")
        self.assertTrue(user_login)
        response = self.client.get("/logout/")
        self.assertRedirects(response, '/search_game/')

from django.test import TestCase
from gamestore.models import UserProfile, Game
from django.contrib.auth.models import User
from gamestore.forms import GameForm, GameUpdateForm

class GameFromsTest(TestCase):

    def setUp(self):
        self.valid_game_form = GameForm(data={
            'name': "Test Name",
            'price': 60.5,
            'category': "ACTION",
            'picture_url': "http://www.vectorfree.com/media/vectors/angry-birds-vector.jpg",
            'description': "The best game ever",
            'game_url': "http://online-gamestore.herokuapp.com/static/games/owngame.html",
            'age_limit': 5,
            'check_agreement': True
        })

        self.invalid_game_form = GameForm(data={
            'name': ".",
            'price': -70.5,
            'category': "ACTIONf",
            'picture_url': 5,
            'description': "",
            'game_url': "Hello",
            'age_limit': -1,
            'check_agreement': False
        })

        self.valid_game_update_form = GameUpdateForm(data={
            'name': "Test Name",
            'price': 60.5,
            'category': "ACTION",
            'picture_url': "http://www.vectorfree.com/media/vectors/angry-birds-vector.jpg",
            'description': "The best game ever",
            'game_url': "http://online-gamestore.herokuapp.com/static/games/owngame.html",
            'age_limit': 6,
        })

        self.invalid_game_update_form = GameUpdateForm(data={
            'name': ".",
            'price': -70.5,
            'category': "ACTIONf",
            'picture_url': 5,
            'description': "",
            'game_url': "Hello",
            'age_limit': -1,
        })

    def test_GameForm_valid(self):
        self.assertTrue(self.valid_game_form.is_valid())

    def test_GameForm_invalid(self):
        self.assertFalse(self.invalid_game_form.is_valid())

    def test_GameUpdateForm_valid(self):
        self.assertTrue(self.valid_game_update_form.is_valid())

    def test_GameUpdateForm_invalid(self):
        self.assertFalse(self.invalid_game_update_form.is_valid())
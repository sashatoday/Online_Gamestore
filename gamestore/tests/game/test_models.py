from datetime import date
from django.db import models
from django.test import TestCase
from gamestore.models import UserProfile, Game

class GameModelTest(TestCase):
    fixtures = ['gamestore.json']

    def _testfieldtype(self, model, modelname, fieldname, type):
        try:
            field = model._meta.get_field(fieldname)
            self.assertTrue(isinstance(field, type), "Testing the type of %s field in model %s"%(fieldname, modelname))
        except FieldDoesNotExist:
            self.assertTrue(False, "Testing if field %s exists in model %s"%(fieldname, modelname))
        return field

    def testFieldTypes(self):
        self._testfieldtype(Game, 'Game', 'name', models.CharField)
        self._testfieldtype(Game, 'Game', 'price', models.FloatField)
        self._testfieldtype(Game, 'Game', 'picture_url', models.URLField)
        self._testfieldtype(Game, 'Game', 'description', models.TextField)
        self._testfieldtype(Game, 'Game', 'game_url', models.URLField)
        self._testfieldtype(Game, 'Game', 'date', models.DateField)
        self._testfieldtype(Game, 'Game', 'category', models.CharField)
        self._testfieldtype(Game, 'Game', 'developer', models.ForeignKey)
        self._testfieldtype(Game, 'Game', 'age_limit', models.PositiveSmallIntegerField)

    def test_field_values(self):
        game = Game.objects.get(id=1)
        self.assertEquals(game.name, 'Test')
        self.assertEquals(game.price, 60.0)
        self.assertEquals(game.picture_url, 'http://www.vectorfree.com/media/vectors/angry-birds-vector.jpg')
        self.assertEquals(game.description, 'Testing')
        self.assertEquals(game.game_url, 'http://online-gamestore.herokuapp.com/static/games/owngame.html')
        self.assertEquals(game.date, date(2019, 2, 17))
        self.assertEquals(game.category, 'ACTION')
        self.assertEquals(game.age_limit, 5)
    
    def test_game_developer(self):
        game = Game.objects.get(id=1)
        developer = UserProfile.objects.get(id=1)
        self.assertEquals(game.get_developer(), developer)

import jsonfield
from datetime import date
from django.db import models
from django.test import TestCase
from gamestore.models import UserProfile, Game, Score

class GameStateModelTest(TestCase):
    fixtures = ['gamestore.json']

    def _testfieldtype(self, model, modelname, fieldname, type):
        try:
            field = model._meta.get_field(fieldname)
            self.assertTrue(isinstance(field, type), "Testing the type of %s field in model %s"%(fieldname, modelname))
        except FieldDoesNotExist:
            self.assertTrue(False, "Testing if field %s exists in model %s"%(fieldname, modelname))
        return field

    def testFieldTypes(self):
        self._testfieldtype(Score, 'Score', 'value', models.PositiveIntegerField)
        self._testfieldtype(Score, 'Score', 'date', models.DateField)
        self._testfieldtype(Score, 'Score', 'scorer', models.ForeignKey)
        self._testfieldtype(Score, 'Score', 'game_in_score', models.ForeignKey)

    def test_field_values(self):
        score = Score.objects.get(id=1)
        self.assertEquals(score.date, date(2019, 2, 18))
        self.assertEquals(score.value, 210)
    
    def test_game_in_score(self):
        score = Score.objects.get(id=1)
        game_in_score = Game.objects.get(id=2)
        self.assertEquals(score.game_in_score, game_in_score)
    
    def test_scorer(self):
        score = Score.objects.get(id=1)
        scorer = UserProfile.objects.get(id=3)
        self.assertEquals(score.scorer, scorer)

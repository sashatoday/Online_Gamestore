import jsonfield
from datetime import date
from django.db import models
from django.test import TestCase
from gamestore.models import UserProfile, Game, GameState

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
        self._testfieldtype(GameState, 'GameState', 'state', jsonfield.JSONField)
        self._testfieldtype(GameState, 'GameState', 'date', models.DateField)
        self._testfieldtype(GameState, 'GameState', 'player', models.ForeignKey)
        self._testfieldtype(GameState, 'GameState', 'game_in_state', models.ForeignKey)

    def test_field_values(self):
        game_state = GameState.objects.get(id=1)
        state = {
            "playerItems" : {
                "beer": 2, 
                "wine": 2, 
                "shot": 2, 
                "water": 1
            },
            "score": 110,
            "type": "SAVE"
        }
        self.assertEquals(game_state.date, date(2019, 2, 18))
        self.assertEquals(game_state.state, state)
    
    def test_game_in_state(self):
        game_state = GameState.objects.get(id=1)
        game_in_state = Game.objects.get(id=2)
        self.assertEquals(game_state.game_in_state, game_in_state)
    
    def test_player(self):
        game_state = GameState.objects.get(id=1)
        player = UserProfile.objects.get(id=3)
        self.assertEquals(game_state.player, player)

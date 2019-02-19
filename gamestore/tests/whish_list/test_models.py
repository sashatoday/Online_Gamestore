from datetime import date
from django.db import models
from django.test import TestCase
from gamestore.models import UserProfile, Game, WishList

class PurchaseModelTest(TestCase):
    fixtures = ['gamestore.json']

    def _testfieldtype(self, model, modelname, fieldname, type):
        try:
            field = model._meta.get_field(fieldname)
            self.assertTrue(isinstance(field, type), "Testing the type of %s field in model %s"%(fieldname, modelname))
        except FieldDoesNotExist:
            self.assertTrue(False, "Testing if field %s exists in model %s"%(fieldname, modelname))
        return field

    def testFieldTypes(self):
        self._testfieldtype(WishList, 'WishList', 'date', models.DateField)
        self._testfieldtype(WishList, 'WishList', 'potential_buyer', models.ForeignKey)
        self._testfieldtype(WishList, 'WishList', 'wished_game', models.ForeignKey)

    def test_date_field_values(self):
        wishlist = WishList.objects.get(id=2)
        self.assertEquals(wishlist.date, date(2019, 2, 18))
    
    def test_get_purchased_game(self):
        wishlist = WishList.objects.get(id=2)
        wished_game = Game.objects.get(id=2)
        self.assertEquals(wishlist.wished_game, wished_game)
    
    def test_potential_buyer(self):
        wishlist = WishList.objects.get(id=2)
        potential_buyer = UserProfile.objects.get(id=3)
        self.assertEquals(wishlist.potential_buyer, potential_buyer)

from datetime import date
from django.db import models
from django.test import TestCase
from gamestore.models import UserProfile, Game, Purchase

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
        self._testfieldtype(Purchase, 'Purchase', 'date', models.DateField)
        self._testfieldtype(Purchase, 'Purchase', 'buyer', models.ForeignKey)
        self._testfieldtype(Purchase, 'Purchase', 'purchased_game', models.ForeignKey)
        self._testfieldtype(Purchase, 'Purchase', 'ref', models.CharField)
        self._testfieldtype(Purchase, 'Purchase', 'complete', models.BooleanField)

    def test_field_values(self):
        purchase = Purchase.objects.get(id=2)
        self.assertEquals(purchase.date, date(2019, 2, 18))
        self.assertEquals(purchase.ref, '29539')
    
    def test_purchase_is_complete(self):
        purchase = Purchase.objects.get(id=2)
        self.assertEquals(purchase.is_complete(), True)
    
    def test_get_purchased_game(self):
        purchase = Purchase.objects.get(id=2)
        game = Game.objects.get(id=1)
        self.assertEquals(purchase.get_purchased_game(), game)
    
    def test_get_buyer(self):
        purchase = Purchase.objects.get(id=2)
        buyer = UserProfile.objects.get(id=3)
        self.assertEquals(purchase.get_buyer(), buyer)

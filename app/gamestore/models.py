from django.db import models
from django.contrib.auth.models import User
from datetime import date
from gamestore.core.constants import *
import jsonfield


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)    
    birthDate = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    country = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=100, blank=True)
    bio = models.TextField(max_length=200, blank=True)
    photoUrl = models.URLField(blank=True)
    role = models.CharField(max_length=1, choices=ROLE_CHOICES, default=PLAYER)
    class Meta:
        ordering = ["user_id"]

    def is_developer(self):
        if self.role == 'D':
            return True
        else:
            return False
 
class Game(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    pictureUrl = models.URLField(blank=True)
    description = models.TextField(max_length=200, blank=True)
    gameUrl = models.URLField()
    date = models.DateField(default=date.today)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    developer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='developer')
    age_limit = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["-date", "name"]
    pass

class Purchase(models.Model):
    date = models.DateField(default=date.today)
    buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='buyer')
    purchasedGame = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='purchasedGame')

    class Meta:
        ordering = ["-date"]
    pass

class Score(models.Model):
    value = models.PositiveIntegerField()
    date = models.DateField(default=date.today)
    scorer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='scorer')
    gameInScore = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='gameInScore')

    class Meta:
        ordering = ["-value"]
    pass

class WishList(models.Model):
    date = models.DateField(default=date.today)
    potentialBuyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='potentialBuyer')
    wishedGame = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='wishedGame')

    class Meta:
        ordering = ["-date"]
    pass

class GameState(models.Model):
    state = jsonfield.JSONField()
    date = models.DateField(default=date.today)
    player = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='player')
    gameInState = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='gameInState')

    class Meta:
        ordering = ["-date"]
    pass
###############################################
##### This file contains following models: ####
#####     * UserProfile                    ####
#####     * Game                           ####
#####     * Purchase                       ####
#####     * Score                          ####
#####     * WishList                       ####
#####     * GameState                      ####
###############################################

from django.db import models
from django.contrib.auth.models import User
from datetime import date
from gamestore.constants import *
import jsonfield


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)    
    birth_date = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=UNKNOWN)
    country = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=100, blank=True)
    bio = models.TextField(max_length=200, blank=True)
    photo_url = models.URLField(blank=True)
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
    picture_url = models.URLField(blank=True)
    description = models.TextField(max_length=500, blank=True)
    game_url = models.URLField()
    date = models.DateField(default=date.today)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    developer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='developer')
    age_limit = models.PositiveSmallIntegerField()

    def get_developer(self):
        return self.developer

    class Meta:
        ordering = ["-date", "name"]

class Purchase(models.Model):
    date = models.DateField(default=date.today)
    buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='buyer')
    purchased_game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='purchased_game')
    ref = models.CharField(max_length=50, blank=True)
    complete = models.BooleanField(default=False)

    def is_complete(self):
        if self.complete == True:
            return True
        else:
            return False

    def get_purchased_game(self):
        return self.purchased_game
    
    def get_buyer(self):
        return self.buyer

    class Meta:
        ordering = ["-date"]

class Score(models.Model):
    value = models.PositiveIntegerField()
    date = models.DateField(default=date.today)
    scorer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='scorer')
    game_in_score = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game_in_score')

    class Meta:
        ordering = ["-value"]

class WishList(models.Model):
    date = models.DateField(default=date.today)
    potential_buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='potential_buyer')
    wished_game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='wished_game')

    class Meta:
        ordering = ["-date"]

class GameState(models.Model):
    state = jsonfield.JSONField()
    date = models.DateField(default=date.today)
    player = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='player')
    game_in_state = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game_in_state')

    class Meta:
        ordering = ["-date"]

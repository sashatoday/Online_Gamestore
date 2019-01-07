from django.db import models
from django.contrib.auth.models import User
from datetime import date

class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)    
    birthYear = models.CharField(max_length=50)
    gender = models.CharField(max_length=5)
    country = models.CharField(max_length=15)
    city = models.CharField(max_length=15)
    address = models.CharField(max_length=15)
    bio = models.TextField()
    photoUrl = models.URLField(blank=True)
    role = models.CharField(max_length=15)
    objects = models.Manager()

class Game(models.Model):
    name = models.CharField(max_length=25, null=False)
    price = models.PositiveIntegerField()
    pictureUrl = models.URLField(blank=True)
    description = models.TextField()
    gameUrl = models.URLField(blank=False)
    date = models.DateField(default=date.today)
    developer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='developer')

    class Meta:
        ordering = ["-date", "name"]
    pass

class Purchase(models.Model):
    date = models.DateField(default=date.today)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer')
    purchasedGame = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='purchasedGame')

    class Meta:
        ordering = ["-date"]
    pass

class Score(models.Model):
    value = models.PositiveIntegerField()
    date = models.DateField(default=date.today)
    scorer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scorer')
    gameInScore = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='gameInScore')

    class Meta:
        ordering = ["-value"]
    pass

class WishList(models.Model):
    date = models.DateField(default=date.today)
    potentialBuyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='potentialBuyer')
    wishedGame = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='wishedGame')

    class Meta:
        ordering = ["-date"]
    pass

class GameState(models.Model):
    state = models.CharField(max_length=50, null=False)
    date = models.DateField(default=date.today)
    player = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player')
    gameInState = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='gameInState')

    class Meta:
        ordering = ["-date"]
    pass
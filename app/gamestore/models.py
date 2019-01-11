from django.db import models
from django.contrib.auth.models import User
from datetime import date

class UserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    UNKNOWN = 'U'
    ADMIN = 'A'
    DEVELOPER = 'D'
    PLAYER = 'P'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (UNKNOWN, 'Unknown'),
    )
    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (DEVELOPER, 'Developer'),
        (PLAYER, 'Player'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)    
    birthDate = models.DateField(null=False, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    country = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=15, blank=True)
    bio = models.TextField(blank=True)
    photoUrl = models.URLField(blank=True)
    role = models.CharField(max_length=1, choices=ROLE_CHOICES, default=PLAYER)

    def get_birth_date(self):
        return self.birthDate
    
class Game(models.Model):
    name = models.CharField(max_length=25, null=False)
    price = models.PositiveIntegerField()
    pictureUrl = models.URLField(blank=True)
    description = models.TextField()
    gameUrl = models.URLField(blank=False)
    date = models.DateField(default=date.today)
    category = models.CharField(max_length=15, blank=True)
    developer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='developer')

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
    state = models.TextField(null=False)
    date = models.DateField(default=date.today)
    player = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='player')
    gameInState = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='gameInState')

    class Meta:
        ordering = ["-date"]
    pass
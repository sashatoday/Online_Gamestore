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
    birthDate = models.DateField()
    age = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    country = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=100, blank=True)
    bio = models.TextField(max_length=200, blank=True)
    photoUrl = models.URLField(blank=True)
    role = models.CharField(max_length=1, choices=ROLE_CHOICES, default=PLAYER)

    def is_developer(self):
        if self.role == 'Developer':
            return True
        else:
            return False

    def get_birth_date(self):
        return self.birthDate

    def get_gender(self):
        return self.gender

    def get_country(self):
        return self.country
    
    def get_city(self):
        return self.city
    
    def get_address(self):
        return self.address

    def get_bio(self):
        return self.bio

    def get_photo_url(self):
        return self.photoUrl
    
    def get_role(self):
        return self.role
    
    
class Game(models.Model):
    CATEGORY_CHOICES = (
        ('ACTION', 'Action'),
        ('ADVENTURE', 'Adventure'),
        ('ARCADE', 'Arcade'),
        ('FANTASY', 'Fantasy'),
        ('FIGHTING', 'Fighting'),
        ('PUZZLE', 'Puzzle'),
        ('SIMULATION', 'Simulation'),
        ('SPORTS', 'Sports'),
        ('STRATEGY', 'Strategy'),
        ('OTHER', 'Other'),
    )
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
    state = models.TextField(null=False)
    date = models.DateField(default=date.today)
    player = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='player')
    gameInState = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='gameInState')

    class Meta:
        ordering = ["-date"]
    pass
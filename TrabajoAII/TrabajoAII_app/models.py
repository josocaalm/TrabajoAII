from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class UserApp(User):
    games = models.ManyToManyField("Game", through="Rating")
    
    def __unicode__(self):
        return self.first_name + ' ' + self.last_name

class Rating(models.Model):
    game = models.ForeignKey("Game")
    userApp = models.ForeignKey("UserApp")
    
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    
    def __str__(self):
        return str(self.rating)

class Game(models.Model):
    name = models.TextField()
    coverString = models.TextField()
    steamID = models.TextField()
    
    def __unicode__(self):
        return self.name
    
class Genre(models.Model):
    usersApp = models.ManyToManyField("UserApp")
    games = models.ManyToManyField("Game")
    
    name = models.TextField()
    
    def __unicode__(self):
        return self.name
    
class SteamTag(models.Model):
    game = models.ManyToManyRel("Game")
    
    tagName = models.TextField()
    
    def __unicode__(self):
        return self.tagName
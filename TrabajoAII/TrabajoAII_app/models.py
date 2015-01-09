from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class UserApp(User):
    games = models.ManyToManyField("Game", through="Rating")
    def __unicode__(self):
        return self.first_name + ' ' + self.last_name

class Rating(models.Model):
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    game = models.ForeignKey("Game")
    userApp = models.ForeignKey("UserApp")
    
    def __str__(self):
        return str(self.puntuacion)

class Game(models.Model):
    name = models.TextField()
    coverString = models.TextField()
    tf2outpostPartialID = models.TextField()
    tf2outpostFullID = models.TextField()
    steamID = models.TextField()
    
    def __unicode__(self):
        return self.name
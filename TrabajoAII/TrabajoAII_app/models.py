from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserApp(User):
    birthdate = models.DateField()
    searchs = models.ManyToManyField("Game", through="Search")


class Search(models.Model):
    user = models.ForeignKey("UserApp")
    shop = models.ForeignKey("Game")


class Game(models.Model):
    name = models.TextField()
    steamID = models.TextField()
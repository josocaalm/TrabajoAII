from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserApp(User):
    birthdate = models.DateField()
    shopRatings = models.ManyToManyField("Shop", through="ShopRating")
    itemRatings = models.ManyToManyField("Item", through="ItemRating")

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name


class ShopRating(models.Model):
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    user = models.ForeignKey("UserApp")
    shop = models.ForeignKey("Shop")
    
    def __unicode__(self):
        return str(self.rating)

class ItemRating(models.Model):
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    user = models.ForeignKey("UserApp")
    item = models.ForeignKey("Item")
    
    def __unicode__(self):
        return str(self.rating)

class Item(models.Model):
    name = models.TextField()
    description = models.TextField()
    category = models.ManyToManyField("Category")
    shops = models.ManyToManyField("Shop", through="Sale")
    
    def __unicode__(self):
        return self.name
    
class Sale(models.Model):
    price = models.FloatField()
    item = models.ForeignKey("Item")
    shop = models.ForeignKey("Shop")
    
    def __unicode__(self):
        return self.item.name
    
class Shop(models.Model):
    name = models.TextField()
    url = models.URLField()
    email = models.EmailField()
    
    def __unicode__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name



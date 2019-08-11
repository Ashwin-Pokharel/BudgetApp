from django.db import models
from django.contrib.auth.models import AbstractUser , User
from datetime import datetime

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    required = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class Incomes(models.Model):
    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100, blank= True)
    price = models.DecimalField(decimal_places=2 , max_digits=20)
    date = models.DateField(auto_now=datetime.today())
    category = models.ForeignKey(Category , on_delete = models.DO_NOTHING , blank = True)
    user = models.ForeignKey(User, on_delete= models.CASCADE , blank=False)

    def __str__(self):
        final_string = "you spent" + str(self.price) + "at" + self.name
        return final_string

class Expense(models.Model):
    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(decimal_places=2 , max_digits=20)
    date = models.DateField(auto_now=datetime.today())
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING , blank= True)
    user = models.ForeignKey(User, on_delete= models.CASCADE , blank= False)

    def __str__(self):
        final_string = "you spent" + str(self.price) + "at" + self.name
        return final_string




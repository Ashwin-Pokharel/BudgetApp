from django.db import models
from django.contrib.auth.models import AbstractUser , User
from datetime import datetime

# Create your models here.

class categoryManager(models.Manager):
    def get_by_natural_key(self , name):
        return self.get(name=name)

class Category(models.Model):
    MY_CHOICES = (
        ('I', 'Income'),
        ('E', 'Expense'),
    )
    name = models.CharField(max_length=50)
    required = models.BooleanField(default=True)
    type = models.CharField(max_length=1 , choices=MY_CHOICES , null=True)
    object = categoryManager()
    def __str__(self):
        return self.name

    def natural_key(self):
        return self.name

class Incomes(models.Model):
    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100, blank= True)
    price = models.DecimalField(decimal_places=2 , max_digits=20)
    date = models.DateField('date')
    category = models.ForeignKey(Category, on_delete = models.DO_NOTHING , blank = True , db_constraint=False , null=True, limit_choices_to={'type':'I'})
    user = models.ForeignKey(User, on_delete= models.CASCADE , blank=False)

    def __str__(self):
        final_string = "you spent" + str(self.price) + "at" + self.name
        return final_string


class Expense(models.Model):
    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(decimal_places=2 , max_digits=20)
    date = models.DateField('date')
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING , blank= True , null=True, db_constraint=False , limit_choices_to={'type':'E'})
    user = models.ForeignKey(User, on_delete= models.CASCADE , blank= False)

    def __str__(self):
        final_string = "you spent" + str(self.price) + "at" + self.name
        return final_string




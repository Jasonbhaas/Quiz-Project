from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Student(models.User):
	username = models.Charfield(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.Password(max_length=50) #TODO will come back to this when looking at authentication the Django User Model
    email = models.CharField(max_length=50) #TODO look into DJANGO email verification

class Quiz_Attempt(models.Model):
    taker = models.ForeignKey(Student)
    test = models.ForeignKey(Quiz)
    score = models.IntegerField()
    start = models.DateField()
    end = models.DateField()

class Question_Attempt(models.Model):

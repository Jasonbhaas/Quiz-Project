from django.db import models
from django import forms
from django.contrib.auth.models import User

# Create your models here.
# class Student(models.Model):
#     username = models.CharField(max_length=30)
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     password = forms.CharField(widget=forms.PasswordInput) #TODO will come back to this when looking at authentication the Django User Model
#     email = models.EmailField(max_length=254) #TODO look into DJANGO email verification
    
#     def __str__(self):
# 	return self.username

class Quiz(models.Model):
    subject = models.CharField(max_length= 50)
    name = models.CharField(max_length=30)
    description = models.TextField()
    instructions = models.TextField()
    author = models.ForeignKey(User)
    
    def __str__(self):
	return self.subject + "-" + self.name

class Question(models.Model):
    quiz = models.ForeignKey(Quiz)
    body = models.TextField()

    def __str__(self):
	return "{}.{}".format(self.quiz, self.body)

class Answer(models.Model):
    body = models.TextField()
    correctness_choices = (
        (1, "Wrong"),
        (2, "Partially Correct"),
        (3, "Correct"))
    point_value = models.IntegerField(choices=correctness_choices, default = 1)
    question = models.ForeignKey(Question)

    def __str__(self):
	return str(self.question) + ".answer"

class Quiz_Attempt(models.Model):
    taker = models.ForeignKey(User)
    test = models.ForeignKey(Quiz)
    score = models.IntegerField()
    start = models.DateField(auto_now = True)
    end = models.DateField()
    submitted = models.BooleanField(default = False)

class Question_Attempt(models.Model):
    quiz = models.ForeignKey(Quiz_Attempt)
    question = models.ForeignKey(Question)
    start = models.DateField()
    end = models.DateField()

class Answer_Attempt(models.Model):
    question = models.ForeignKey(Question_Attempt)
    answer = models.ForeignKey(Answer)

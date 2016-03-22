from django.db import models

# Create your models here.
class Student(models.Model):
	username = models.Charfield(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput) #TODO will come back to this when looking at authentication the Django User Model
    email = models.EmailField(max_length=254) #TODO look into DJANGO email verification

class Quiz_Attempt(models.Model):
    taker = models.ForeignKey(Student)
    test = models.ForeignKey(Quiz)
    score = models.IntegerField()
    start = models.DateField()
    end = models.DateField()

class Question_Attempt(models.Model):
    quiz = models.ForeignKey(Quiz_Attempt)
    question = models.ForeignKey(Question)
    start = models.DateField()
    end = models.DateField()

class Answer_attempt(models.Model):
    question = models.ForeignKey(Question_Attempt)
    answer = models.ForeignKey(Answer)

class Quix(models.Model):
    subject = models.CharField(max_length= 50)
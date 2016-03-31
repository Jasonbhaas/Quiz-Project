from django.db import models
from django import forms


# Create your models her

# class Quiz(models.Model):
#     subject = models.CharField(max_length= 50)
#     name = models.CharField(max_length=30)
#     description = models.TextField()
#     instructions = models.TextField()
#     author = models.ForeignKey(User)
    
#     def __str__(self):
# 	return self.subject + "-" + self.name

class Question(models.Model):
    quiz = models.ForeignKey(Quiz)
    body = models.TextField()
    order = models.IntegerField()

    def __str__(self):
	return "{}.{}".format(self.quiz, self.order)

class Answer(models.Model):
    body = models.TextField()
    point_value = models.IntegerField()
    question = models.ForeignKey(Question)

    def __str__(self):
	return str(self.question) + ".answer"

class Quiz_Attempt(models.Model):
    taker = models.ForeignKey(User)
    test = models.ForeignKey(Quiz)
    score = models.IntegerField()
    start = models.DateField()
    end = models.DateField()

class Question_Attempt(models.Model):
    quiz = models.ForeignKey(Quiz_Attempt)
    question = models.ForeignKey(Question)
    start = models.DateField()
    end = models.DateField()

class Answer_Attempt(models.Model):
    question = models.ForeignKey(Question_Attempt)
    answer = models.ForeignKey(Answer)

from django.db import models
from django import forms
from django.contrib.auth.models import User


class Quiz(models.Model):
    subject = models.CharField(max_length=50)
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
    point_value = models.IntegerField(choices=correctness_choices, default=1)
    question = models.ForeignKey(Question)

    def __str__(self):
        return str(self.body)


class Quiz_Attempt(models.Model):
    taker = models.ForeignKey(User)
    test = models.ForeignKey(Quiz)
    score = models.IntegerField(null=True)
    start = models.DateField(auto_now=True)
    end = models.DateField(null=True)
    submitted = models.BooleanField(default=False)


class Question_Attempt(models.Model):
    quiz = models.ForeignKey(Quiz_Attempt)
    question = models.ForeignKey(Question)
    start = models.DateTimeField(auto_now=True)
    end = models.DateTimeField(null=True)


class Answer_Attempt(models.Model):
    question = models.ForeignKey(Question_Attempt)
    answer = models.ForeignKey(Answer)

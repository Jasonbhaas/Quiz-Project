from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from models import Quiz, Question, Answer, Quiz_Attempt


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password1")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        exclude = ()


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ()


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        exclude = ()


class Quiz_AttemptForm(forms.ModelForm):
    class Meta:
        model = Quiz_Attempt
        fields = ("taker", "test")

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from models import Quiz, Question, Answer, Quiz_Attempt, Answer_Attempt


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
        widgets = {
            'author': forms.HiddenInput(),
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ()
        widgets = {
            'quiz': forms.HiddenInput(),
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        exclude = ()
        widgets = {
            'question': forms.HiddenInput(),
        }


class Quiz_AttemptForm(forms.ModelForm):
    class Meta:
        model = Quiz_Attempt
        fields = ("taker", "test")


class Answer_AttemptForm(forms.ModelForm):
    class Meta:
        model = Answer_Attempt
        exclude = ()
        widgets = {
            'question': forms.HiddenInput(),
            'answer': forms.HiddenInput(),
        }


class Quiz_Attempt_SubmitForm(forms.ModelForm):
    class Meta:
        model = Quiz_Attempt
        exclude = ('score', 'start')
        widgets = {
            'taker': forms.HiddenInput(),
            'test': forms.HiddenInput(),
            'end': forms.HiddenInput(),
            'submitted': forms.HiddenInput()}

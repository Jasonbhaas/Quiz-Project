from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # ex: /quiz/
    url(r'^$', views.index, name='index'),
    url(r'^quiz/(?P<quiz_id>[0-9]+)/$', views.quiz, name='quiz'),
    url(r'^(?P<question_id>[0-9]+)/question/$', views.question, name='question'),
    url(r'^quiz/new/$', views.make_quiz, name='make_quiz'),
    url(r'^quiz/(?P<quiz_id>[0-9]+)/new/question', views.write_question, name="write_question"),
    url(r'^question/(?P<question_id>[0-9]+)/new/answer', views.write_answer, name="write_answer"),
    url(r'^sign_up', views.create_user, name="sign_up"),
    url(r'^log_in', views.log_in, name="log_in"),
    url(r'^log_out', views.log_out, name="log_out"),
    url('^change_password/', auth_views.password_change),
    url(r'^take_quiz', views.take_quiz, name="take_quiz"),
    url(r'^take/(?P<quiz_id>[0-9]+)', views.begin_quiz, name="begin_quiz"),
]

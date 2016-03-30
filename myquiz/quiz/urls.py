from django.conf.urls import url

from . import views

urlpatterns = [
	# ex: /quiz/
	url(r'^$', views.index, name='index'),
	url(r'^quiz/(?P<quiz_id>[0-9]+)/$', views.quiz, name='quiz'),
	url(r'^(?P<question_id>[0-9]+)/question/$', views.question, name='question'),
	url(r'^quiz/new/$', views.make_quiz, name='make_quiz'),
	url(r'^quiz/new/quiz_create', views.create_quiz),
	url(r'^quiz/(?P<quiz_id>[0-9]+)/new/question', views.write_question, name="write_question"),
]

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect,  Http404
from django .template import loader
from django .shortcuts import render
from models import Quiz

from models import Quiz

def index(request):
	quizzes = Quiz.objects.all()
	template = loader.get_template('quiz/index.html')
	context = {
		'quizzes' : quizzes
	}
	return HttpResponse(template.render(context, request))

def quiz(request, quiz_id):
	try:
		quiz = Quiz.objects.get(pk=quiz_id)
	except Quiz.DoesNotExist:
		raise Http404("Quiz does not exist")
	return render(request, 'quiz/quiz.html', {'quiz': quiz})

def question(request, question_id):
	response = "You're looking at the question %s."
	return HttpResponse(response % question_id)

def make_quiz(request):
	#add in some authentication here I believe
	return render(request, 'quiz/make_quiz.html')

def create_quiz(request):
	quiz = Quiz(name = request.POST['name'],  subject = request.POST['subject'],
		instructions = request.POST['instructions'], description = request.POST['description'])
	quiz.save()
	return HttpResponseRedirect('/')

def write_question(request, quiz_id):
	try:
		quiz = Quiz.objects.get(pk=quiz_id)
   	except Quiz.DoesNotExist:
        	raise Http404("Quiz does not exist")
	return render(request, 'quiz/write_question.html', {'quiz': quiz})

def register(request):
	return render(request, 'quiz/register')

def create_user(request):
	pass

# Create your views here


from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect,  Http404
from django .template import loader
from django .shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from forms import UserCreateForm, QuizForm, QuestionForm, AnswerForm, Quiz_AttemptForm, Answer_AttemptForm
from models import Quiz, Question, Answer, Quiz_Attempt, Question_Attempt, Answer_Attempt


def index(request):
    quizzes = Quiz.objects.all()
    template = loader.get_template('quiz/index.html')
    context = {
        'quizzes': quizzes
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


@login_required
def make_quiz(request):
    quizzes = Quiz.objects.all()
    if request.method == "POST":
        data = request.POST
        data_copy = dict()
        for key, value in data.iteritems():
            data_copy[key] = value
            data_copy['author'] = request.user.id
        form = QuizForm(data_copy)
        if form.is_valid():
            form.save(request.user)
            return HttpResponseRedirect('/')
    else:
        form = QuizForm()
    return render(request, 'quiz/make_quiz.html', context={'form':form, 'quizzes':quizzes})


def write_question(request, quiz_id):
    try:
        quiz = Quiz.objects.get(pk=quiz_id)
    except Quiz.DoesNotExist:
            raise Http404("Quiz does not exist")
    if request.method=="POST":
        data = request.POST
        mydata = dict()
        for key, value in data.iteritems():
            mydata[key] = value
            mydata['quiz'] = quiz_id
        form = QuestionForm(mydata)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('')
    else:
        questions = Question.objects.all().filter(quiz=quiz_id)
        form = QuestionForm()
    return render(request, 'quiz/write_question.html', {'quiz': quiz, 'form': form, 'questions' : questions})


def write_answer(request, question_id):
    answers = Answer.objects.all().filter(question=question_id)
    try:
        question = Question.objects.get(pk=question_id)
    except Quiz.DoesNotExist:
            raise Http404("Question does not exist")
    if request.method == "POST":
        data = request.POST
        mydata = dict()
        for key, value in data.iteritems():
            mydata[key] = value
            mydata['question'] = question_id
        form = AnswerForm(mydata)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('')
    else:
        form = AnswerForm()
    return render(request, 'quiz/write_answer.html', {'question': question, 'form': form, 'answers': answers})


def create_user(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = UserCreateForm()
    return render(request, 'quiz/create_user.html', context={'form':form})


def log_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                # account is disabled
                return HttpResponseRedirect('/account_disabled')
        else:
            # invalid logint
            return HttpResponseRedirect('/invalid_login')
    else:
        return render(request, 'quiz/log_in.html')


def log_out(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def take_quiz(request):
    quizzes = Quiz.objects.all()
    new_quizzes= []
    in_progress_quizzes= []
    for quiz in quizzes:
        try:
            attempt = Quiz_Attempt.objects.get(taker=request.user.id, test=quiz.id)
            if attempt.submitted == False:
                in_progress_quizzes += [quiz]
        except Quiz_Attempt.DoesNotExist:
            new_quizzes += [quiz]
    return render(request, 'quiz/take_quiz.html', context={'new_quizzes': new_quizzes, 'in_progress_quizzes': in_progress_quizzes})


@login_required
def confirm_quiz(request, quiz_id):
    try:
        quiz = Quiz.objects.get(pk=quiz_id)
    except Quiz.DoesNotExist:
        raise Http404("Quiz does not exist")

    try:
        attempt = Quiz_Attempt.objects.get(taker=request.user.id, test=quiz_id)
        if attempt.submitted:
            return HttpResponseRedirect('already taken this quiz')
        else:
            return HttpResponseRedirect('/take/{{quiz.id}}')
    except Quiz_Attempt.DoesNotExist:
        return render(request, 'quiz/test_confirm.html', context={'quiz': quiz})
        # make new quiz attempt for them. We sould expect this
   

@login_required
def begin_quiz(request, quiz_id):
    try:
        quiz = Quiz.objects.get(pk=quiz_id)
    except Quiz.DoesNotExist:
        raise Http404("Quiz does not exist")
    questions = Question.objects.filter(quiz = quiz_id).order_by('id')
    question = questions[0]
    try:
        attempt = Quiz_Attempt.objects.get(taker=request.user.id, test=quiz_id)
    except Quiz_Attempt.DoesNotExist:
        data = {'test': quiz_id, 'taker': request.user.id}
        form = Quiz_AttemptForm(data)
        if form.is_valid():
            form.save()
            attempt = Quiz_Attempt.objects.get(taker=request.user.id, test=quiz_id)
        # make new quiz attempt for them. We sould expect this
    if attempt.submitted:
        return HttpResponseRedirect('already taken this quiz')
    else:
        return render(request, 'quiz/instructions.html', context={'quiz': quiz, 'question': question})

@login_required
def answer_question(request, quiz_id, question_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    question = Question.objects.get(pk=question_id)
    quiz_attempt = Quiz_Attempt.objects.get(taker=request.user.id, test=quiz_id)
    if quiz_attempt.submitted:
        return HttpResponseRedirect('already taken this quiz')
    else:
        try:
            question_attempt = Question_Attempt.objects.get(quiz=quiz_attempt, question= question)
        except Question_Attempt.DoesNotExist:
            question_attempt = Question_Attempt(quiz=quiz_attempt, question= question)
            question_attempt.save()

    if request.method== "POST":
        try:
            post_question = request.POST['question']
            post_answer = request.POST['answer']
            answer_attempt = Answer_Attempt.objects.get(question= post_question, answer= post_answer)
            answer_attempt.delete()
        except Answer_Attempt.DoesNotExist:
            form = Answer_AttemptForm(request.POST)
            if form.is_valid():
                form.save(request.user)
    
    answers = Answer.objects.filter(question = question_id)
    forms = []
    for answer in answers:
        try:
            answer_attempt = Answer_Attempt.objects.get(question= question_attempt.id, answer= answer.id)
            forms += [[answer, True, Answer_AttemptForm( {'question': question_attempt.id, 'answer': answer.id})]]
        except Answer_Attempt.DoesNotExist:
            forms += [[answer, False, Answer_AttemptForm({'question': question_attempt.id, 'answer': answer.id})]]
    return render(request, 'quiz/answer_question.html', context={'quiz': quiz, 'forms':forms, 'question': question, 'answers': answers})
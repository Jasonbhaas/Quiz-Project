from django.shortcuts import render
import datetime
from django.http import HttpResponse, HttpResponseRedirect,  Http404
from django .template import loader
from django .shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from forms import UserCreateForm, QuizForm, QuestionForm, AnswerForm, Quiz_AttemptForm, Answer_AttemptForm, Quiz_Attempt_SubmitForm
from models import Quiz, Question, Answer, Quiz_Attempt, Question_Attempt, Answer_Attempt


def index(request):
    """Returns the home page with quizzes avaialble"""
    quizzes = Quiz.objects.all()
    template = loader.get_template('quiz/index.html')
    context = {
        'quizzes': quizzes
    }
    return HttpResponse(template.render(context, request))


@user_passes_test(lambda u: u.is_superuser)
def make_quiz(request):
    """Shows all current quizes and lets users make new ones"""
    quizzes = Quiz.objects.all()
    if request.method == "POST":
        # copies form data to a new dictionary and adds the user as author
        data = request.POST
        data_copy = dict()
        for key, value in data.iteritems():
            data_copy[key] = value
            data_copy['author'] = request.user.id
        form = QuizForm(data_copy)
        if form.is_valid():
            form.save(request.user)
            return HttpResponseRedirect('/quiz/new')
    else:
        form = QuizForm()
    return render(request, 'quiz/make_quiz.html', context={'form': form, 'quizzes': quizzes})


@user_passes_test(lambda u: u.is_superuser)
def write_question(request, quiz_id):
    """Shows all questions for a quiz and lets user create a new one"""
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    if request.method == "POST":
        # copies the form data to a new dictionary and adds the quiz id
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
    return render(request, 'quiz/write_question.html', {'quiz': quiz, 'form': form, 'questions': questions})


@user_passes_test(lambda u: u.is_superuser)
def write_answer(request, question_id):
    """Shows all answers for a question and allows user to create a new one"""
    answers = Answer.objects.all().filter(question=question_id)
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        # copies the form data to a new dictionary and adds the question id
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
    """Creates a new user"""
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = UserCreateForm()
    return render(request, 'quiz/create_user.html', context={'form': form})


def log_in(request):
    """authenticates the user and begins session"""
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/account_disabled')
        else:
            return HttpResponseRedirect('/invalid_login')
    else:
        return render(request, 'quiz/log_in.html')


def log_out(request):
    """ends session for a user"""
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def take_quiz(request):
    """Shows all quizes a user can take"""
    quizzes = Quiz.objects.all()
    new_quizzes = []
    in_progress_quizzes = []
    for quiz in quizzes:
        try:
            attempt = Quiz_Attempt.objects.get(taker=request.user.id, test=quiz.id)
            if attempt.submitted is False:
                in_progress_quizzes += [quiz]
        except Quiz_Attempt.DoesNotExist:
            new_quizzes += [quiz]
    return render(request, 'quiz/take_quiz.html', context={'new_quizzes': new_quizzes, 'in_progress_quizzes': in_progress_quizzes})


@login_required
def confirm_quiz(request, quiz_id):
    """Shows the description of the quiz"""
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    try:
        attempt = Quiz_Attempt.objects.get(taker=request.user.id, test=quiz_id)
        if attempt.submitted:
            return HttpResponseRedirect('/take_quiz')
        else:
            return HttpResponseRedirect('/take/{{quiz.id}}')
    except Quiz_Attempt.DoesNotExist:
        return render(request, 'quiz/test_confirm.html', context={'quiz': quiz})


@login_required
def begin_quiz(request, quiz_id):
    """Checks that a quiz attempt exists or creates a new one"""
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = Question.objects.filter(quiz=quiz_id).order_by('id')
    question = questions[0]
    try:
        attempt = Quiz_Attempt.objects.get(taker=request.user.id, test=quiz_id)
    except Quiz_Attempt.DoesNotExist:
        data = {'test': quiz_id, 'taker': request.user.id}
        form = Quiz_AttemptForm(data)
        if form.is_valid():
            form.save()
            attempt = Quiz_Attempt.objects.get(taker=request.user.id, test=quiz_id)
    if attempt.submitted:
        return HttpResponseRedirect('/take_quiz')
    else:
        return render(request, 'quiz/instructions.html', context={'quiz': quiz, 'question': question})


@login_required
def answer_question(request, quiz_id, question_id):
    """lets user create answer attempts for questions

    Checks that a quiz and question attempt exist or creates a new one
    Creates an answer attempt if one does not exist
    Deletes an answer attempt if one does exist
    """
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    question = get_object_or_404(Question, pk=question_id, quiz=quiz_id)
    questions = list(Question.objects.filter(quiz=quiz_id).order_by('id'))
    index = questions.index(question)
    # Gets the previous and next question
    try:
        next_q = questions[index+1].id
    except IndexError:
        next_q = "submit"
    if index == 0:
        prev_q = ""
    else:
        prev_q = questions[index-1].id

    quiz_attempt = get_object_or_404(Quiz_Attempt, taker=request.user.id, test=quiz_id)
    # looks for a question attempt and makes one if one doesn't already exist
    if quiz_attempt.submitted:
        return HttpResponseRedirect('/take_quiz')
    else:
        try:
            question_attempt = Question_Attempt.objects.get(quiz=quiz_attempt, question=question)
        except Question_Attempt.DoesNotExist:
            question_attempt = Question_Attempt(quiz=quiz_attempt, question=question)
            question_attempt.save()
    # Uses the form data to look for an existing answer attempt. Deletes it if
    # it finds one, and saves the form if one does not exist
    if request.method == "POST":
        try:
            post_question = request.POST['question']
            post_answer = request.POST['answer']
            answer_attempt = Answer_Attempt.objects.get(question=post_question, answer=post_answer)
            answer_attempt.delete()
        except Answer_Attempt.DoesNotExist:
            form = Answer_AttemptForm(request.POST)
            if form.is_valid():
                form.save(request.user)

    answers = Answer.objects.filter(question=question_id)
    forms = []
    # creates forms for each answer, and records if an answer attempt exists
    for answer in answers:
        try:
            answer_attempt = Answer_Attempt.objects.get(question=question_attempt.id, answer=answer.id)
            forms += [[answer.body, True, Answer_AttemptForm({'question': question_attempt.id, 'answer': answer.id})]]
        except Answer_Attempt.DoesNotExist:
            forms += [[answer.body, False, Answer_AttemptForm({'question': question_attempt.id, 'answer': answer.id})]]
    return render(request, 'quiz/answer_question.html', context={'quiz': quiz, 'forms': forms, 'question': question,
                  'answers': answers, 'index': index, 'next_q': next_q, 'prev_q': prev_q})


@login_required
def quiz_submit(request, quiz_id):
    """Updates the quiz_attempt with a score and endtime"""
    if request.method == "POST":
        attempt = Quiz_Attempt.objects.get(taker=request.user.id, test=quiz_id)
        attempt.end = datetime.datetime.now()
        attempt.submitted = True
        attempt.score = score(attempt)
        attempt.save()
        return HttpResponseRedirect('/take_quiz')
    form = Quiz_Attempt_SubmitForm()
    return render(request, 'quiz/submit.html', context={'quiz_id': quiz_id, 'form': form})


@login_required
def review(request):
    """shows all taken quizes and the scores"""
    try:
        quizzes = Quiz_Attempt.objects.filter(taker=request.user.id)
        return render(request, 'quiz/review.html', context={'quizzes': quizzes})
    except Quiz_Attempt.DoesNotExist:
        return HttpResponseRedirect('/take_quiz')


def score(attempt):
    """Returns the score for a quiz attempt"""
    score = 0
    question_attempts = Question_Attempt.objects.filter(quiz=attempt.id)
    for q in question_attempts:
        tally = [0, 0, 0]
        answers = Answer_Attempt.objects.filter(question=q)
        for a in answers:
            tally[a.answer.point_value-1] += 1
        score += (0**tally[0])*(.5**tally[1])*tally[2]
    return score

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from models import *
from views import *
from django.contrib.auth import authenticate, login, logout

class ModelsTestCase(TestCase):
    """this tests all the modesl by creating instances"""
    def test_user(self):
        """tests that users were successfully created"""
        user = User.objects.create(username='jason', password="secret")
        self.assertEqual(user.username, 'jason')
        self.assertEqual(user.password, 'secret')

    def test_quiz(self):
        """tests that quizzes were successfully created"""
        [user, quiz, questions, answers] = create_quiz()
        self.assertEqual(quiz.subject, 'math')
        self.assertEqual(quiz.author.username, 'test')

    def test_questions(self):
        """tests that questions were successfully created"""
        [user, quiz, questions, answers] = create_quiz()
        self.assertEqual(questions[0].body, 'The first question')
        self.assertEqual(len(Question.objects.all()), 3)

    def test_answers(self):
        """tests that answers were successfully created"""
        [user, quiz, questions, answers] = create_quiz()
        self.assertEqual(answers[0].body, 'correct')
        self.assertEqual(len(Answer.objects.all()), 9)


class IndexViewsTestCase(TestCase):
    """Tests that index works properly"""
    def test_index(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)


class Take_QuizViewsTestCase(TestCase):
    """Tests for taking a quiz"""
    def test_take_quiz_no_quizzes(self):
        """Tests take_quiz works even if there are no quizzes"""
        user = User.objects.create(username='testuser', email='test@123.com', password='hello', is_active=True)
        c = Client()
        c.login(username=user.username, password='hello')
        response = c.get('/take_quiz/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_take_quiz_quizzes(self):
        """tests take_quiz when quizzes do exist"""
        create_quiz()
        user = User.objects.create(username='testuser', password='hello', is_active=True)
        c = Client()
        c.login(username='testuser', password='hello')
        response = c.get('/take_quiz/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_begin_quiz_no_attempt(self):
        """tests that begin_quiz creates a quiz attempt"""
        [user, quiz, questions, answers] = create_quiz()
        c = Client()
        c.login(username=user.username, password='hello')
        url = 'take/{}'.format(quiz.id)
        c.get(url)
        self.assertIsNotNone(Quiz_Attempt.get.objects.get(taker=user.id))

    def test_begin_quiz_already_started(self):
        """tests that begin_quiz doesn't make an extra quiz attempt"""
        [user, quiz, questions, answers] = create_quiz()
        c = Client()
        Quiz_Attempt.create(test=quiz.id, taker=user.id)
        c.login(username=user.username, password='hello')
        url = 'take/{}'.format(quiz.id)
        c.get(url)
        self.assertEqual(len(Quiz_Attempt.objects.all()), 1)

    def test_question_attempt_no_attempt(self):
        """tests that question_attempt creates an question attempt if new Q"""
        [user, quiz, questions, answers] = create_quiz()
        Quiz_attempt = Quiz_Attempt.objects.create(test=quiz.id, taker=user.id)
        c = Client()
        c.login(username=user.username, password='hello')
        url = 'take/{}/{}'.format(quiz.id, questions[0].id)
        c.get(url)
        self.assertIsNotNone(Quiz_Attempt.get.objects.all())

    def test_question_attempt_already_created(self):
        """tests that question_attempt does not make a duplicate question attempt"""
        [user, quiz, questions, answers] = create_quiz()
        Quiz_attempt = Quiz_Attempt.objects.create(test=quiz.id, taker=user.id)
        question_attempt = Question_Attempt.objects.create(quiz=Quiz_attempt.id, question=questions[0].id)
        c = Client()
        c.login(username=user.username, password='hello')
        url = 'take/{}/{}'.format(quiz.id, questions[0].id)
        c.get(url)
        self.assertEqual(len(Question_Attempt.objects.all()), 1)


    def test_answer_attempt_no_attempt(self):
        """tests that answer_attempt creates an answer attempt if seleted"""
        [user, quiz, questions, answers] = create_quiz()
        Quiz_attempt = Quiz_Attempt.objects.create(test=quiz.id, taker=user.id)
        question_attempt = Question_Attempt.objects.create(quiz=Quiz_attempt.id, question=questions[0].id)
        answer_attempt = Answer_Attempt.objects.create(question = question_attempt.id, answer=answers[1].id)
        c = Client()
        c.login(username=user.username, password='hello')
        url = 'take/{}/{}'.format(quiz.id, questions[0].id)
        c.get(url)
        self.assertEqual(len(Answer_Attempt.objects.all()), 2)

    def test_answer_attempt_already_selected(self):
        """tests that answer_attempt deletes the answer attempt if deselected"""
        [user, quiz, questions, answers] = create_quiz()
        Quiz_attempt = Quiz_Attempt.objects.create(test=quiz.id, taker=user.id)
        question_attempt = Question_Attempt.objects.create(quiz=Quiz_attempt.id, question=questions[0].id)
        answer_attempt = Answer_Attempt.create(question=question_attempt.id, answer=answers[0].id)
        c = Client()
        c.login(username=user.username, password='hello')
        url = 'take/{}/{}'.format(quiz.id, questions[0].id)
        c.get(url)
        self.assertIsNone(Answer_Attempt.get.objects.all)



def create_quiz():
    """template for creating a quiz. makes 1 quiz, 3 qs and 9 answers"""
    user = User.objects.create(username='test', password='hello', is_active=True)
    quiz = Quiz.objects.create(subject='math', author=user, instructions='test instructions', description='test description')
    question1 = Question.objects.create(quiz=quiz, body='The first question')
    question2 = Question.objects.create(quiz=quiz, body='The second question')
    question3 = Question.objects.create(quiz=quiz, body='The third question')
    answer11 = Answer.objects.create(body='correct', point_value=3, question=question1)
    answer12 = Answer.objects.create(body='semi-correct', point_value=2, question=question1)
    answer13 = Answer.objects.create(body='wrong', point_value=1, question=question1)
    answer21 = Answer.objects.create(body='correct', point_value=3, question=question2)
    answer22 = Answer.objects.create(body='correct', point_value=2, question=question2)
    answer23 = Answer.objects.create(body='correct', point_value=1, question=question2)
    answer31 = Answer.objects.create(body='correct', point_value=3, question=question3)
    answer32 = Answer.objects.create(body='correct', point_value=2, question=question3)
    answer33 = Answer.objects.create(body='correct', point_value=1, question=question3)
    questions = [question1, question2, question3]
    answers = [answer11, answer12, answer13, answer21, answer22, answer23,
               answer31, answer32, answer33]
    return [user, quiz, questions, answers]

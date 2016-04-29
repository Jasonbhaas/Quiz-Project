from django.test import TestCase
from models import Quiz, Question, Answer, Quiz_Attempt, Question_Attempt, Answer_Attempt


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

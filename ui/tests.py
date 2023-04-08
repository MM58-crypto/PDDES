from django.test import TestCase
from ui.models import Question, Choice
#from django.utils import timezone 
# Create your tests here.


class Question_Test_Case(TestCase):
    # model tests 
    def create_question(self):
        Question.objects.create(question_text="How are ya?(test)")

    def test_question_creation(self):
        q = self.create_question()
        self.assertTrue(isinstance(q, Question))
        self.assertEqual(q.__unicode__(), q.question_text)

#found a bug #1, foreign key mismatch
# "ui_choice" referencing "ui_question"


from django.test import TestCase
from models import Question, Quiz, Answer, Employee, UserAttempt
from django.urls import reverse

# Create your tests here.
# the goal here is to create tests to see if all the pages are going where they need to.
# the page should be appropriately redirected once it hits an endpoint

class QuizHomeTests(TestCase):
    def test_quiz_display(self):
        response = self.clent.get(reverse("quiz:quiz_home"))
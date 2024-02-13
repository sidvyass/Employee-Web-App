import datetime
from django.db import models
from django.contrib.auth.models import User


DEPARTMENT_CHOICES = [
        ("HR", "Human Resources"),
        ("IT", "Information Technology"),
        ("FN", "Finance"),
        ("MK", "Marketing"),
        ("QL", "Quality"),
]

class Department(models.Model):
    """we will control who views what through this"""
    name = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES, unique=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def get_department(self):
        return self.department

# parent class that everything else will inherit from
class Quiz(models.Model):
    title = models.CharField(max_length=100, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        """have to change this as we cannot have such a big string rep, here for debugging"""
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class UserAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    best_score = models.IntegerField(default=0)
    time_taken = models.IntegerField(default=0)  # this is to be able to add it to the table first
    date_taken = models.DateTimeField("Date Taken", null=True, auto_now_add=True)

    class Meta:
        unique_together = ('user', 'quiz')

    def __str__(self):
        score_value = str(self.score)
        return self.quiz.title + score_value

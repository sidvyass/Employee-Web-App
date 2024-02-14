from typing import Any
from quiz.models import Quiz, Answer, Question, Department
from django.core.management import BaseCommand
from django.core.management.base import CommandParser


class Command(BaseCommand):
    help = "Database is populated with whatever the API returns"

    # def add_arguments(self, parser: CommandParser) -> None:
        # parser.add_argument adds an argument that we can access through the command line.
        # parser.add_argument("filepath", type=str, help="path of the file that has the gpt output")
        # parser.add_argument("")  # quiz name

    def handle(self, *args: Any, **options: Any) -> str | None:
        # file_path = options['filepath']
        file_path = r"C:\PythonProjects\sample_generated_quiz.txt"
        # these values are default as of now
        department = Department.objects.get(pk=1)
        quiz, created = Quiz.objects.get_or_create(title="cl_quiz1", department=department)

        self.stdout.write(self.style.SUCCESS(f'Processing file: {file_path} title = {quiz} department = {department}'))
                
        with open(file_path) as file:
            lines = file.readlines()
            key = ""
            for line in  lines:
                if line.startswith("**"):
                    key = line
                    question = Question(text=line.strip("**"), quiz=quiz)
                    question.save()
                    self.stdout.write(self.style.SUCCESS(f"Question registered successfully id - {question.id} - {question}"))
                elif not line.startswith("---") and key != "":
                    temp = line.strip().split("-")
                    if len(temp) == 3:
                        is_correct = temp[2].strip() == 'true'
                        answer = Answer(text=temp[1], question=question, is_correct=is_correct)
                        answer.save()
                        self.stdout.write(self.style.SUCCESS(f"Answer registered successfully id - {answer.id} - {answer}"))
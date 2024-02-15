from typing import Any
from quiz.models import Quiz, Answer, Question, Department
from django.core.management import BaseCommand
from django.core.management.base import CommandParser


class Command(BaseCommand):
    help = "Database is populated with whatever the API returns"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("filepath", type=str, help="path of the file that has the gpt output")
        parser.add_argument("department_id", type=int, help="Deparment id range(5)")
        parser.add_argument("quiz_name", type=str, help="The name of the new quiz")

    def handle(self, *args: Any, **options: Any) -> str | None:
        file_path = options['filepath']
        try:
            department = Department.objects.get(pk=options['department_id'])
            quiz, created = Quiz.objects.get_or_create(title=options["quiz_name"], department=department)

            self.stdout.write(self.style.SUCCESS(f'Processing file: {file_path} title = {quiz} department = {department}'))
        except Department.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Department does not exist, department id can only be -> {[x+1 for x, y in enumerate(Department.objects.all())]}"))
                
        with open(file_path) as file:
            lines = file.readlines()
            key = ""
            for line in  lines:
                if line.startswith("**"):
                    key = line
                    question = Question(text=line.strip("**\n"), quiz=quiz)
                    question.save()
                    self.stdout.write(self.style.SUCCESS(f"Question registered successfully id - {department.name} - {question.text}"))
                elif not line.startswith("---") and key != "":
                    temp = line.strip().split("-")
                    if len(temp) == 3:
                        is_correct = temp[2].strip() == 'true'
                        answer = Answer(text=temp[1], question=question, is_correct=is_correct)
                        answer.save()
                        self.stdout.write(self.style.SUCCESS(f"\tAnswer registered successfully id: {answer.text} - {answer.is_correct}"))

        # quiz.delete()
        # self.stdout.write(self.style.SUCCESS(f"Deleted"))

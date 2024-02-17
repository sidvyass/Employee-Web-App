from typing import Any
from django.db import IntegrityError, transaction
from django.core.management import BaseCommand
from django.core.management.base import CommandParser
from django.contrib.auth.models import User
from quiz.models import Employee, Department
import pyodbc
from user_login.data import conn_string, query

def pull_username_password():
    conn = pyodbc.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute(query)
    # firstname, lastname, code, password, departmentFK
    return cursor.fetchall()

class Command(BaseCommand):
    # purpose -> Pulling data from Mie Trak, updating the values or creating a new user if they dont exist.
    help = "pulls data from Mie Trak and updated the database"

    def handle(self, *args: Any, **options: Any) -> str | None:
        user_list = pull_username_password()
        for user in user_list: 
            # username is already a string returned from Mie Trak
            first_name, last_name, username, password = user[0], user[1], user[2], str(user[3])
            try:
                new_user = User.objects.get(username=username)
                new_user.set_password(password)
                new_user.save()
                self.stdout.write(self.style.SUCCESS(f"SUCCESS in user -> {first_name + " " + last_name}"))
            except User.DoesNotExist:
                new_user = User.objects.create(username=username)
                new_user.set_password(password)
                new_user.save()
                self.stdout.write(self.style.ERROR(f"ERROR in user add manually to databae -> {first_name + " " + last_name}"))
            # if user[4]:
            #     department = Department.objects.get(pk=user[4]) 
            # else:
            #     department = Department.objects.get(pk=211) 
            # print(f"Values -> {username, password, department}")
            # try:
            #     with transaction.atomic():
            #         new_user, user_created = User.objects.get_or_update(first_name=first_name, last_name=last_name, username=username, defaults={'password':password})
            #         new_employee, employee_created = Employee.objects.get_or_create(user=new_user, defaults={'department':department})
            #         if user_created and employee_created:
            #             self.stdout.write(self.style.SUCCESS(f"CREATED USER -> {new_user}"))
            #             self.stdout.write(self.style.SUCCESS(f"CREATED EMPLOYEE -> {new_employee}"))
            #         else:
            #             self.stdout.write(self.style.SUCCESS(f"EXISTED USER -> {new_user}"))
            #             self.stdout.write(self.style.SUCCESS(f"EXISTED EMPLOYEE -> {new_employee}"))
            #         self.stdout.write(self.style.SUCCESS(f"Created new user"))
            # except IntegrityError as e:
            #     print(f"Integrity error - {e}")

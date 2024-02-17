from django.core.management import BaseCommand
from django.db.utils import IntegrityError
from typing import Any
from django.core.management.base import CommandParser
from quiz.models import Department
import pyodbc
from user_login.data import conn_string

def pull_departments():
   conn = pyodbc.connect(conn_string)
   cursor = conn.cursor()
   query = "SELECT DepartmentPK, Name FROM department"
   cursor.execute(query)
   return cursor.fetchall()

class Command(BaseCommand):
   help = "Pulls department from Mie Trak and puts it into the database. The id in Mie trak is also the Id in this database" 

   def handle(self, *args: Any, **options: Any) -> str | None:
        departments = pull_departments()
        self.stdout.write(self.style.SUCCESS(f"Total departments pulled from Mie Trak - {len(departments)}")) 
        count = 0
        for department in departments:
            new_department_id, new_department_name = department[0], department[1]
            try:
                new_department_obj, created_bool = Department.objects.update_or_create(id=new_department_id, defaults={'name': new_department_name})
                if created_bool:
                    self.stdout.write(self.style.SUCCESS(f"Object was CREATED - {new_department_obj}")) 
                else:
                    self.stdout.write(self.style.SUCCESS(f"Object was UPDATED - {new_department_obj}"))
                count += 1
            except IntegrityError:
                print(department)

        self.stdout.write(self.style.SUCCESS(f"All objects entered successfully. Count - {count}")) 

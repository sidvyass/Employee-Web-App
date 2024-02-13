from django.contrib import admin
from .models import Question, Answer, UserAttempt, Quiz, Department

# Register your models here.
admin.site.register(Department)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(UserAttempt)

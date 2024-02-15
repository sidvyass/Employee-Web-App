from django.contrib import admin
import nested_admin
from .forms import QuestionForm
from .models import Question, Answer, UserAttempt, Quiz, Department

# Register your models here.
admin.site.register(Department)
admin.site.register(UserAttempt)

class AnswerInLine(nested_admin.NestedStackedInline):
    model = Answer
    form = QuestionForm
    extra = 4  # Controls how many empty new forms are displayed

class QuestionInLine(nested_admin.NestedStackedInline):
    model = Question
    inlines = [AnswerInLine]  # This nests AnswerInline within QuestionInline
    extra = 1  # Controls how many empty new forms are displayed

class QuizAdmin(nested_admin.NestedModelAdmin):
    model = Quiz
    inlines = [QuestionInLine]
    list_display = ('title', 'department')  # This displays fields in the Quiz admin list view

# admin.site.register(Question, QuestionAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.site_header = "Etz Admin"
admin.site.site_title = "Etz Admin"

from django.urls import path
from . import views

app_name = "quiz"

urlpatterns = [
    path("home", views.quizhome, name="quiz_home"),
    path("choose_department", views.choose_department, name="choose_department"),
    path("scores", views.scores, name="scores"),
    path("<int:quiz_pk>/quiz_detail_landing", views.quiz_detail_landing, name="landing_page"),
    path("<int:quiz_pk>/quiz_detail", views.quiz_detail, name="quiz_detail"),
]

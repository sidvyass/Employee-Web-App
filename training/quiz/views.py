from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, UserAttempt, Answer, Employee, Department
from django.urls import reverse
from django.http import HttpResponse

# Create your views here.

@login_required(login_url="/login")
def quizhome(request):
    user = request.user
    try:
        department = user.employee.department
    except Employee.DoesNotExist:
        return redirect(reverse("choose_department"))

    return render(request, "quiz/home.html", {"quiz":Quiz.objects.all()})

def choose_department(request):
    """In case department is not selected"""
    user = request.user
    if request.method == "POST":
        department_choice = Department.objects.get(id=request.POST.get("department"))
        # print(department_choice)
        employee, created = Employee.objects.get_or_create(user=user, department=department_choice)
        employee.save()
        return redirect(reverse("quiz_home"))
    else:
        return render(request, "quiz/choose_department.html", {"departments": Department.objects.all()})

@login_required(login_url="/login")
def quiz_detail(request, quiz_pk):
    if request.method == "POST":
        quiz = get_object_or_404(Quiz, pk=quiz_pk)
        user = request.user
        time = int(request.POST.get('time_taken'))
        answer_ids = []

        try:
            attempt = UserAttempt.objects.get(user=user, quiz=quiz)
        except UserAttempt.DoesNotExist:
            attempt = UserAttempt(user=user, quiz=quiz)
            attempt.time_taken = time

        if time < attempt.time_taken:
            attempt.time_taken = time
        attempt.score = 0

        for ques in quiz.question_set.all():
            selected_answer = request.POST.get(f'selected_answers_{ques.id}')
            if selected_answer:  # to ensure that if a question is not answered we dont get an error 
                if Answer.objects.get(id=selected_answer).is_correct:
                    answer_ids.append(int(selected_answer))
                    attempt.score += 1
                    attempt.save()

        if attempt.score > attempt.best_score:
            attempt.best_score = attempt.score
            attempt.save()

        print(answer_ids)
        return render(request, "quiz/quiz_results.html", {"score":attempt.score,
                                                          "quiz":quiz,
                                                          "correct_answer":answer_ids}) 
    else:
        quiz = get_object_or_404(Quiz, pk=quiz_pk)
        return render(request, "quiz/quiz_detail.html", {"quiz": quiz})

def quiz_detail_landing(request, quiz_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    try:
        attempt = UserAttempt.objects.get(user=request.user, quiz=quiz)
        best_score = attempt.best_score
    except UserAttempt.DoesNotExist:
        best_score = 0

    return render(request, "quiz/quiz_landing_page.html", {"quiz":quiz, "best_score": best_score})


@login_required(login_url="/login")
def scores(request):
    user = request.user
    attempts = UserAttempt.objects.filter(user=user)
    return render(request, "quiz/scores.html", {"user_attempt":attempts})

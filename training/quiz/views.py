from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, UserAttempt, Answer, Employee, Department, Question
from django.urls import reverse
from django.http import HttpResponse


@login_required(login_url="/login")
def quizhome(request):
    user = request.user
    try:
        department = user.employee.department.all()
        print(department)
    except Employee.DoesNotExist:
        return redirect(reverse("choose_department"))

    quiz = Quiz.objects.filter(department__in=department)
    # for q in quiz:
    #     print(q)
    return render(request, "quiz/home.html", {"quiz":quiz})


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
        # TODO: time is not in the correct format
        time = int(request.POST.get('time_taken'))
        answer_ids = []
        
        attempt, created = UserAttempt.objects.get_or_create(user=user, quiz=quiz)
        if time < attempt.time_taken:
            attempt.time_taken = time

        # score has to be zero before we start calculating
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

        return render(request, "quiz/quiz_results.html", {"score":attempt.score,
                                                          "quiz":quiz,
                                                          "time_taken": attempt.time_taken,
                                                          "correct_answer":answer_ids}) 
    else:
        quiz = get_object_or_404(Quiz, pk=quiz_pk)
        return render(request, "quiz/quiz_detail.html", {"quiz": quiz})


@login_required(login_url="/login")
def quiz_detail_landing(request, quiz_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    try:
        attempt = UserAttempt.objects.get(user=request.user, quiz=quiz)
        best_score = attempt.best_score
    except UserAttempt.DoesNotExist:
        best_score = 0

    return render(request, "quiz/quiz_landing_page.html", {"quiz":quiz, "best_score": best_score, "count": quiz.question_set.count()})


@login_required(login_url="/login")
def scores(request):
    user = request.user
    attempts = UserAttempt.objects.filter(user=user)
    print(attempts)
    return render(request, "quiz/scores.html", {"user_attempt":attempts})


@login_required(login_url="/login")
def take_quiz(request, quiz_pk, ques_no):
    user = request.user
    quiz = Quiz.objects.get(pk=quiz_pk)

    if not quiz.question_set.all():
        return HttpResponse("There are no questions in this quiz")

    question_set = [ques.id for ques in quiz.question_set.all()]
    question_no = ques_no + 1
    attempt, created = UserAttempt.objects.get_or_create(user=user, quiz=quiz)

    try:
        # context = quiz, question
        if request.method == "POST":
            answer_id = request.POST.get("selected")  # we get the id of the answer from here
            if Answer.objects.get(pk=answer_id).is_correct:
                attempt.score += 1
                print(attempt.score)
                attempt.save()

            question = Question.objects.get(pk=question_set[ques_no])
            return render(request, "quiz/take_quiz.html", {"quiz":quiz, "question":question, "ques_id":question_no})
        else:
            attempt.score = 0
            attempt.save()
            question = Question.objects.get(pk=question_set[ques_no])
            return render(request, "quiz/take_quiz.html", {"quiz":quiz, "question":question, "ques_id":question_no})
    except IndexError:
        if attempt.score > attempt.best_score:
            attempt.best_score = attempt.score
        attempts = UserAttempt.objects.filter(user=user)
        return render(request, "quiz/scores.html", {"user_attempt": attempts})

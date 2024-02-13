from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from quiz.models import Employee
from django.urls import reverse


@login_required(login_url="/login")
def home(request):
    return render(request, "user_login/home.html")


# the only reason we need to handle this is bc we want to display our own form
def sign_up(request):
    # here the register button and the url going to the sign up page both pertain to this function
    # when we get a POST method we handle user creation
    # when we get a GET request we just display the form
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():  # both is_valid and .save come with django
            user = form.save()  # save the user info to database login(request, user)
            department = form.cleaned_data.get('department')
            Employee.objects.create(user=user, department=department)
            login(request, user)
            return redirect(reverse('quiz_home'))
    else:
        form = RegisterForm()
    
    # "form":form context is important as it displays the crispy forms 
    return render(request, 'registration/sign_up.html', {"form": form})


# we have to handle this as a post request hence we need this function
def logout_user(request):
    logout(request)
    return redirect('/login')

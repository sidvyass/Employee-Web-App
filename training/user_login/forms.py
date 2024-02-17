from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from quiz.models import DEPARTMENT_CHOICES

# this adds the following "fields" to the user model. We are extending
# the user-creation-form class to be able to take in email
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES, required=True)

    class Meta:
        model = User
        fields = ["username", "email", "department", "password1", "password2"]

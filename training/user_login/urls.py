from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # path("", views.home, name="home"),
    # path("home/", views.home, name="home"),
    path("sign-up/", views.sign_up, name="sign-up"),
    path("logout/", views.logout_user, name="logout"),
]

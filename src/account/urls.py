from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("register/", LoginView.as_view(template_name="account/register.html"), name="log_in"),
    path("logout/", LogoutView.as_view(), name="log_off"),
]

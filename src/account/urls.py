from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("register/", views.LoginView.as_view(), name="log_in"),
    path("logout/", views.LogoutView.as_view(), name="log_off"),
]

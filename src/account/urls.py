from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("register/", views.log_in, name="log_in"),
    path("logout/", views.log_off, name="log_off"),
]

from django.urls import path

from . import views

# URLConf
urlpatterns = [
    path("", views.home_page),
    path("register/", views.register),
    path("quizes/", views.quizes),
    path("contact/", views.contact),
]

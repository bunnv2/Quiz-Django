from django.urls import path

from . import views

# URLConf
urlpatterns = [
    path("", views.home_page, name="hello"),
    path("register/", views.register, name="register"),
    path("quizes/", views.quizes, name="quizes"),
]

from django.urls import path

from . import views

urlpatterns = [
    path("quizes/", views.quizes, name="quizes"),
]

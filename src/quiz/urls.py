from django.urls import path

from . import views

urlpatterns = [
    path("quizes/", views.quizes, name="quizes"),
    path("quizes/<int:quiz_id>/", views.quiz_view, name="quiz"),
]

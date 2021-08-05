from django.urls import path

from . import views

urlpatterns = [
    path("quizes/", views.quizes, name="quizes"),
    path("quizes/<int:quiz_id>/", views.quiz_view, name="quiz"),
    path("quizes/results/", views.quiz_view, name="results"),
    path("quizes/quiz-creation/", views.quiz_creator, name="creator"),
    path("quizes/quesion-creation/", views.quiz_creator, name="que-creator"),
]

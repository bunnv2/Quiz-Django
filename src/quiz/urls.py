from django.urls import path

from . import views

urlpatterns = [
    path("quizes/", views.QuizListView.as_view(), name="quizes"),
    path("quizes/<int:quiz_id>/", views.QuizView.as_view(), name="quiz"),
    path("quizes/results/", views.QuizView.as_view(), name="results"),
    path("quizes/quiz-creation/", views.QuizCreatorView.as_view(), name="creator"),
    path("quizes/quesion-creation/", views.QuizCreatorView.as_view(), name="que-creator"),
]

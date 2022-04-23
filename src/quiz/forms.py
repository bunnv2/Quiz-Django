from django.forms import ModelForm

from .models import Question, Quiz


class QuizCreationForm(ModelForm):
    class Meta:
        model = Quiz
        fields = [
            "title",
            "time",
            "required_score_to_pass",
        ]


class QuestionCreationForm(ModelForm):
    class Meta:
        model = Question
        fields = [
            "question",
            "correct_answer",
            "answer_one",
            "answer_two",
            "answer_three",
        ]

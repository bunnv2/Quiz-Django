import random

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Quiz(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Tytuł",
    )
    time = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name="Czas na ukończenie",
    )
    required_score_to_pass = models.IntegerField(
        verbose_name="Wymagana liczba punktów",
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Quizes"


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        verbose_name="Quiz",
        related_name="questions",
        related_query_name="question",
    )
    question = models.CharField(
        max_length=254,
        verbose_name="Treść pytania",
    )
    correct_answer = models.CharField(max_length=255, verbose_name="Poprawna odpowiedź")
    answer_one = models.CharField(max_length=255, verbose_name="Odpowiedź")
    answer_two = models.CharField(max_length=255, verbose_name="Odpowiedź")
    answer_three = models.CharField(max_length=255, verbose_name="Odpowiedź")

    def get_mixed_answers(self):
        """Get mixed answers as key-value pairs aka dict"""

        answers = {
            0: self.correct_answer,
            1: self.answer_one,
            2: self.answer_two,
            3: self.answer_three,
        }

        item_list = list(answers.items())
        random.shuffle(item_list)
        answers = dict(item_list)
        return answers.values()

    def is_answer_correct(answer_id: int):
        return answer_id == 0

    def __str__(self):
        return "{} {}".format(self.quiz.title, self.question)

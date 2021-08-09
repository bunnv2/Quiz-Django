import random

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse


class Quiz(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Tytuł",
        unique=True,
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

    def is_quiz_passed(self, points):
        if points >= self.required_score_to_pass:
            return True
        else:
            return False

    def is_required_time(self, seconds):
        if seconds >= self.time:
            return False
        return True

    def get_absolute_url(self):
        return reverse("quiz:quiz", kwargs={"quiz_id": self.pk})

    def get_add_question_url(self):
        return reverse("quiz:question-creator", kwargs={"quiz_id": self.pk})

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
        return dict(item_list)

    def is_answer_correct(self, answer_id: int):
        return answer_id == self.get_correct_answer()

    def get_correct_answer(self):
        return 0

    def __str__(self):
        return "{} {}".format(self.quiz.title, self.question)


class QuizResults(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        verbose_name="Quiz",
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name="Użytkownik",
    )
    quiz_start = models.DateTimeField(auto_now=False, auto_now_add=False)
    quiz_end = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    results = models.IntegerField(
        verbose_name="Liczba punktów",
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
    )

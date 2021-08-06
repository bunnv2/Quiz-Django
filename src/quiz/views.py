from datetime import datetime
from re import template

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View

from .models import Question, Quiz, QuizResults


class QuizListView(View):
    template_name = "quiz/quizes.html"

    def get(self, request):
        quizes = Quiz.objects.all()
        context = {
            "quizes": quizes,
        }
        return render(request, "quiz/quizes.html", context)


class QuizView(View):
    template_name = "quiz/quiz_view.html"
    second_template_view = "quiz/results_view.html"

    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        questions = Question.objects.filter(quiz=quiz)
        context = {
            "quiz": quiz,
            "questions": questions,
        }
        session, created = QuizResults.objects.get_or_create(
            quiz=quiz,
            user=User.objects.get(id=request.user.id),
            quiz_end=None,
            defaults={"quiz_start": datetime.now()},
        )
        return render(request, self.template_name, context)

    def post(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        questions = Question.objects.filter(quiz=quiz)
        context = {
            "quiz": quiz,
            "questions": questions,
        }

        results = 0
        answers_selected = {}
        answers_correct = {}

        for question in questions:
            answer = request.POST.get(f"question_{question.id}", [""])[0]

            if answer.isnumeric():
                answer = int(answer)
            else:
                answer = None

            answers_selected[question.id] = answer

            if answer is None or not question.is_answer_correct(answer):
                continue

            answers_correct[question.id] = answer
            results += 1

        quiz_result = results / questions.count() * 100

        obj = QuizResults.objects.get(quiz=quiz, user=request.user, quiz_end=None)
        obj.quiz_end = timezone.now()
        obj.results = quiz_result
        obj.save()

        delta = obj.quiz_end - obj.quiz_start

        context["required_time"] = quiz.is_required_time(delta.seconds)
        context["delta"] = delta.seconds
        context["answers_selected"] = answers_selected
        context["results"] = obj
        context["passed"] = quiz.is_quiz_passed(obj.results)
        context["questions"] = questions
        return render(request, self.second_template_view, context)


class QuizCreatorView(View):
    template_name = "quiz/quiz_creator.html"
    second_template_name = "quiz/question_creator.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        title = request.POST.get(f"quiz-title")
        time = request.POST.get(f"quiz-time")
        score = request.POST.get(f"quiz-score")
        new_quiz, created = Quiz.objects.get_or_create(
            title=title,
            defaults={
                "time": time,
                "required_score_to_pass": score,
            },
        )
        quizes = Quiz.objects.exclude(title=title)

        # TODO: THROW AN EXCEPTION FOR ALREADY EXISTING QUIZ
        #       adding questions, and answers, after adding - add again

        # new_question = Question (
        #     quiz=Quiz.objects.get(id=request.POST.get(f"dropdown")),
        #     question=request.POST.get(f"question"),
        #     correct_answer=request.POST.get(f"correct_answer"),
        #     answer_one=request.POST.get(f"answer_one"),
        #     answer_two=request.POST.get(f"answer_two"),
        #     answer_three=request.POST.get(f"answer_three"),
        # )

        # new_question.save()

        context = {
            "new_quiz": new_quiz,
            "quizes": quizes,
        }

        return render(request, self.second_template_name, context)

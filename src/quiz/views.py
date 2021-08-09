from datetime import datetime

from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View

from .forms import QuestionCreationForm, QuizCreationForm
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

        if questions.count() > 0:
            quiz_result = results / questions.count() * 100
        else:
            quiz_result = 0

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
    form_class = QuizCreationForm

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST)

        if not form.is_valid():
            return render(request, self.template_name, {"form": form})

        quiz = form.save()

        return redirect(quiz.get_add_question_url())


class QuestionCreatorView(View):
    template_name = "quiz/question_creator.html"
    form_class = QuestionCreationForm

    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        questions = Question.objects.filter(quiz=quiz)

        return render(
            request,
            self.template_name,
            {
                "form": self.form_class(),
                "quiz": quiz,
                "questions": questions,
            },
        )

    def post(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        form = self.form_class(request.POST)

        if not form.is_valid():
            return render(request, self.template_name, {"form": form})

        question = form.save(commit=False)
        question.quiz = quiz
        question.save()
        return redirect(quiz.get_add_question_url())

from datetime import datetime
from typing import List

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from .forms import QuestionCreationForm, QuizCreationForm
from .models import Question, Quiz, QuizResults


class QuizListView(View):
    template_name = "quiz/quizes.html"
    # model = Quiz

    def get_queryset(self):
        qs = super(QuizListView, self).get_queryset()
        qs = Quiz.objects.filter(Q(author=self.request.user) | Q(is_published=True))
        return super().get_queryset()

    def get_context_data(self, quizes):

        context = super().get_context_data()

        quizes = Quiz.objects.filter(Q(author=self.request.user) | Q(is_published=True))

        if self.request.user.is_superuser:
            quizes = Quiz.objects.all()

        context["quizes"] = quizes
        return context

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, "quiz/quizes.html")

        quizes = Quiz.objects.filter(Q(author=request.user) | Q(is_published=True))

        if request.user.is_superuser:
            quizes = Quiz.objects.all()

        context = {
            "quizes": quizes,
        }
        return render(request, "quiz/quizes.html", context)


class QuizView(LoginRequiredMixin, View):
    login_url = "account:log_in"
    redirect_field_name = "quiz/quiz_view.html"
    template_name = "quiz/quiz_view.html"
    second_template_view = "quiz/results_view.html"

    def get(self, request, quiz_id):
        # View quiz questions and start timer
        if not request.user.is_authenticated:
            return render(request, "quiz/quizes.html")

        quiz = get_object_or_404(Quiz, pk=quiz_id)
        questions = Question.objects.filter(quiz=quiz)
        context = {
            "quiz": quiz,
            "questions": questions,
        }
        QuizResults.objects.get_or_create(
            quiz=quiz,
            user=User.objects.get(id=request.user.id),
            quiz_end=None,
            defaults={"quiz_start": datetime.now()},
        )
        return render(request, self.template_name, context)

    def post(self, request, quiz_id):
        # Check if answers are correct, sum time and display results and other statistics

        quiz = get_object_or_404(Quiz, pk=quiz_id)
        share = request.POST.get("share", None)

        if share is not None:
            if quiz.author != request.user:
                return redirect("quiz:quizes")
            quiz.is_published = not quiz.is_published
            quiz.save()
            return redirect("quiz:quizes")

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


class QuizCreatorView(LoginRequiredMixin, CreateView):
    template_name = "quiz/quiz_creator.html"
    form_class = QuizCreationForm
    login_url = "account:log_in"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return redirect(self.get_success_url())


class QuestionCreatorView(LoginRequiredMixin, CreateView):
    login_url = "account:log_in"
    template_name = "quiz/question_creator.html"
    form_class = QuestionCreationForm
    pk_url_kwarg = "quiz_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["quiz"] = get_object_or_404(Quiz, pk=self.kwargs[self.pk_url_kwarg])
        context["questions"] = Question.objects.filter(quiz=context["quiz"])
        return context

    def form_valid(self, form):
        quiz = get_object_or_404(Quiz, pk=self.kwargs[self.pk_url_kwarg])

        question = form.save(commit=False)
        question.quiz = quiz
        question.save()
        return redirect(quiz.get_add_question_url())

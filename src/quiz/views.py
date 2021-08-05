from datetime import datetime, timedelta
from time import time

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render

from .models import Question, Quiz, QuizResults


def quizes(request):
    """Add all quizes to context and then iterate over them in template"""
    quizes = Quiz.objects.all()
    context = {
        "quizes": quizes,
    }
    return render(request, "quiz/quizes.html", context)


def quiz_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    context = {
        "quiz": quiz,
        "questions": questions,
    }
    if request.method != "POST":
        session, created = QuizResults.objects.get_or_create(
            quiz=quiz,
            user=User.objects.get(id=request.user.id),
            quiz_end=None,
            defaults={"quiz_start": datetime.now()},
        )
        return render(request, "quiz/quiz_view.html", context)

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

    QuizResults.objects.filter(quiz=quiz, user=request.user, quiz_end=None).update(
        quiz_end=datetime.now(),
        results=quiz_result,
    )

    obj = QuizResults.objects.latest("quiz_start")
    delta = obj.quiz_end - obj.quiz_start

    context["required_time"] = quiz.is_required_time(delta.seconds)
    context["delta"] = delta.seconds
    context["answers_selected"] = answers_selected
    context["results"] = quiz_result
    context["passed"] = quiz.is_quiz_passed(context["results"])
    context["questions"] = questions
    return render(request, "quiz/results_view.html", context)

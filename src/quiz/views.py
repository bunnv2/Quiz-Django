from django.shortcuts import get_object_or_404, render

from .models import Question, Quiz


def quizes(request):
    """Add all quizes to context and then iterate over them in template"""
    quizes = Quiz.objects.all()
    context = {
        "quizes": quizes,
    }
    return render(request, "quiz/quizes.html", context)


def quiz_view(request, quiz_id):
    """Choose which quiz you want to be redirected to"""
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    answers = [bool]
    context = {
        "quiz": quiz,
        "questions": questions,
        "answers": answers,
    }

    if request.method != "POST":
        return render(request, "quiz/quiz_view.html", context)

    for question in questions:
        answer = request.POST.get(f"question_{question.id}", [None])[0]

        if not (answer == "0" or answer == "1" or answer == "2" or answer == "3" or answer == None):
            print(f"nice try! ;) id: {answer}, question: {question.id}")
            continue

        if not answer or not question.is_answer_correct(int(answer)):
            print(f"do better: id: {answer}, question: {question.id}")
            continue

        print(f"good job!: id: {answer}, question: {question.id}")
        answers.append(True)

    return render(request, "quiz/quiz_view.html", context)

from django.shortcuts import render


def quizes(request):
    return render(request, "quiz/quizes.html", {})

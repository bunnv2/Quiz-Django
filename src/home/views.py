from django.http import HttpResponse
from django.http.request import HttpHeaders
from django.shortcuts import render

# request - > response
# request handler / action


def home_page(request):
    return render(request, "home/home.html", {})


def quizes(request):
    return render(request, "home/quizes.html", {})

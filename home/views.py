from django.http import HttpResponse
from django.shortcuts import render

# request - > response
# request handler / action

def say_hello(request):
    return HttpResponse("Hello World!")

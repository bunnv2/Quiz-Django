from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from account.forms import SignUpForm


def register(request):
    if not request.user.is_authenticated:
        return render(request, "account/register.html", {})
    else:
        return redirect("home:home")


def signup(request):
    if request.user.is_authenticated:
        return redirect("home:home")

    if request.method != "POST":
        return render(request, "account/signup.html", {"form": SignUpForm()})

    form = SignUpForm(request.POST)

    if not form.is_valid():
        return render(request, "account/signup.html", {"form": form})

    form.save()
    user = authenticate(
        username=form.cleaned_data.get("username"),
        password=form.cleaned_data.get("password1"),
    )
    login(request, user)
    return redirect("home:home")


def log_in(request):
    if request.user.is_authenticated:
        return redirect("home:home")
    if request.method != "POST":
        return render(request, "account/register.html", {"form": AuthenticationForm()})

    form = AuthenticationForm(request=request, data=request.POST)

    if not form.is_valid():
        return render(request, "account/register.html", {"form": form})

    user = authenticate(
        username=form.cleaned_data["username"],
        password=form.cleaned_data["password"],
    )
    if user:
        login(request, user)
        return redirect("home:home")

    return render(request, "account/register.html", {"form": form})


def log_off(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("home:home")

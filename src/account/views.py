from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.views import View

from account.forms import SignUpForm


class RegisterView(View):
    template_name = "account/register.html"

    def get(self, request):
        if not request.user_is_authenticated:
            return render(request, self.template_name)
        return redirect("home:home")


class SignupView(View):
    template_name = "account/signup.html"
    redirect_to = "home:home"
    form_class = SignUpForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(self.redirect_to)
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST)

        if not form.is_valid():
            return render(request, self.template_name, {"form": form})

        form.save()
        user = authenticate(
            username=form.cleaned_data.get("username"),
            password=form.cleaned_data.get("password1"),
        )
        login(request, user)
        return redirect(self.redirect_to)


class LoginView(View):
    template_name = "account/register.html"
    redirect_to = "home:home"
    form_class = AuthenticationForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(self.redirect_to)
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request):
        form = self.form_class(request=request, data=request.POST)

        if not form.is_valid():
            return render(request, self.template_name, {"form": form})

        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )
        if user:
            login(request, user)
            return redirect(self.redirect_to)

        return render(request, self.template_name, {"form": form})


class LogoutView(View):
    redirect_to = "home:home"

    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect(self.redirect_to)

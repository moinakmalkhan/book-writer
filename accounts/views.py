from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views import View

from accounts.forms import LoginForm, SignUpForm


class SignUpView(View):
    """
    View to create a new user.
    """
    def post(self, request):
        form = SignUpForm(request, request.POST)
        if form.is_valid():
            form.save()
            return redirect('books:home')
        return render(request, "accounts/signup.html", {"form": form})

    def get(self, request):
        form = SignUpForm(request)
        return render(request, "accounts/signup.html", {"form": form})


class LoginView(View):
    """
    View to log a user in.
    """
    def post(self, request):
        form = LoginForm(request, request.POST)
        if form.is_valid():
            login(request, form.cleaned_data["user"])
            next = request.GET.get('next') or 'books:home'
            return redirect(next)
        return render(request, "accounts/login.html", {"form": form})

    def get(self, request):
        form = LoginForm(request)
        return render(request, "accounts/login.html", {"form": form})


def user_logout(request):
    """
    View to log a user out.
    """
    logout(request)
    return redirect("accounts:login")

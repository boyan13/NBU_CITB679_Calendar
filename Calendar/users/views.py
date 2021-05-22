from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login
from django.urls import reverse
from .forms import UserCreationFormWithEmail


def dashboard(request):
    return render(request, "users/dashboard.html")


def register(request):

    if request.method == "GET":

        return render(
            request, "users/register.html",
            {"form": UserCreationFormWithEmail}
        )

    elif request.method == "POST":

        form = UserCreationFormWithEmail(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("dashboard"))
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse
from .forms import UserCreationFormWithEmail


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
            return redirect(reverse("calendar"))
        else:
            print(form.errors)
            return render(
                request, "users/register.html",
                {"form": UserCreationFormWithEmail}
            )
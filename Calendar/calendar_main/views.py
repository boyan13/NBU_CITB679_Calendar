from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def calendar(request):
    return render(request, "calendar.html")
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.calendar, name='calendar'),
    path('create/', views.create, name="create")
]

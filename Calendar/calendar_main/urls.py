from django.urls import path

from . import views


urlpatterns = [
    path('', views.calendar, name='calendar'),
    path('save/', views.save, name="save"),
    path('delete/', views.delete, name="delete"),
    path('edit/', views.edit, name="edit")
]

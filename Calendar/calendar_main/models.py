from django.db import models
from django.conf import settings

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=255)
    for_date = models.DateTimeField()
    day_of_week = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
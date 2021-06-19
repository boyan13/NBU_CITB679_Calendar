from django.db import models
from django.conf import settings

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(default = None, blank = True, null = True)
    day_of_week = models.IntegerField(default = None, blank = True, null = True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
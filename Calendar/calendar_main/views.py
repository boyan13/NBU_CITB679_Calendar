import traceback
import json

from django.shortcuts import render
from django.http import JsonResponse

from django.core.handlers.wsgi import WSGIRequest
# from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.decorators import login_required

from . import models
from django.core import serializers

def calendar(request: WSGIRequest):
    context = {'calendar_events': []}

    if request.user.is_authenticated:
        calendar_events= []
        events = models.Event.objects.filter(created_by=request.user.id)
        
        for event in events:
            calendar_events.append({
                "id": event.pk,
                "title": event.title
            })
        context["calendar_events"] = calendar_events

    return render(request, "calendar.html", context)

@csrf_exempt
def create(request: WSGIRequest):
    response = {'isSuccessful': False}

    if request.method == "POST":
        req_body = json.loads(request.body)
        try:
            events = []
            for event in req_body["events"]:
                events.append(models.Event(
                    created_by=request.user.id,
                    title=event['title'],
                    day_of_week=5,
                    start_time=event['title'],
                    end_time=event['title'],
                    for_date=event['title']
                ))

        except Exception as exc:
            # Print exception in terminal (since we have no logging)
            traceback.format_exc(exc)
            print(exc)
            # Handle
            response["isSuccesful"] = False
            return JsonResponse(response)

    return JsonResponse({})


def update(request):
    return

import traceback
import json

from django.shortcuts import render
from django.http import JsonResponse

from django.core.handlers.wsgi import WSGIRequest
# from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.decorators import login_required

from . import models


def calendar(request: WSGIRequest):
    context = {'calendar_events': []}

    if request.user.is_authenticated:
        events = models.Event.objects.filter(created_by=request.user.id)
        context['calendar_events'] = events

    return render(request, "calendar.html", context)


@csrf_exempt
def create(request):
    response = {'isSuccessful': False}

    if request.method == "POST":
        req_body = json.loads(request.body)
        try:
            events = []
            for ev in req_body["events"]:
                events.append(models.Event(
                    created_by=request.user.id,
                    title=ev['title'],
                    day_of_week=5,
                    start_time=ev['title'],
                    end_time=ev['title'],
                    for_date=ev['title']
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

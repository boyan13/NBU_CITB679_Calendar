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
from datetime import datetime

def calendar(request: WSGIRequest):
    context = {'calendar_events': []}

    if request.user.is_authenticated:
        calendar_events= []
        events = models.Event.objects.filter(created_by=request.user.id)
        
        for event in events:
            calendar_events.append({
                "id": event.pk,
                "title": event.title,
                "start": event.start_date.isoformat(),
                "end" : event.end_date.isoformat() if (event.end_date is not None) else None,
                "allDay" : True if (event.end_date is None) else False
            })
        context["calendar_events"] = calendar_events

    return render(request, "calendar.html", context)

@csrf_exempt
def save(request: WSGIRequest):
    response = {'isSuccessful': False}

    if request.method == "POST":
        req_body = json.loads(request.body)
        try:
            eventsForUpdate = []
            eventsForCreate = []

            for event in req_body["events"]:
                    eventModel = models.Event(
                        title=event["title"],
                        start_date=event["start"],
                        end_date= None if (event["allDay"] is True) else event["end"],
                        created_by = request.user,
                        created_on=datetime.utcnow()
                    )

                    if not event["id"]:
                        eventsForCreate.append(eventModel)
                    else:
                        eventModel.pk = event["id"]
                        eventsForUpdate.append(eventModel)

            models.Event.objects.bulk_update(eventsForUpdate, ['title', 'start_date', 'end_date'])
            models.Event.objects.bulk_create(eventsForCreate)
        except Exception as exc:
            # Print exception in terminal (since we have no logging)
            traceback.format_exc(exc)
            print(exc)
            # Handle
            response["isSuccesful"] = False
            return JsonResponse(response)

    return JsonResponse({})
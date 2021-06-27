import traceback
import json
from datetime import datetime

from django.shortcuts import render
from django.http import JsonResponse
from django.core.handlers.wsgi import WSGIRequest

from . import models


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


def save(request: WSGIRequest):
    response = {'isSuccessful': False}

    if request.method == "POST":
        req_body = json.loads(request.body)
        try:
            events_for_update = []
            events_for_create = []

            for event in req_body["events"]:
                model = models.Event(
                    title=event["title"],
                    start_date=event["start"],
                    end_date=None if (event["allDay"] is True) else event["end"],
                    created_by=request.user,
                    created_on=datetime.utcnow()
                )

                if not event["id"]:
                    events_for_create.append(model)
                else:
                    model.pk = event["id"]
                    events_for_update.append(model)

            models.Event.objects.bulk_update(events_for_update, ['title', 'start_date', 'end_date'])
            models.Event.objects.bulk_create(events_for_create)

        except Exception as exc:
            # Print exception in terminal (since we have no logging)
            traceback.format_exc(exc)
            print(exc)
            # Handle
            response["isSuccesful"] = False
            return JsonResponse(response)

    return JsonResponse({})


def delete(request: WSGIRequest):
    model_id = json.loads(request.body)['id']
    models.Event.objects.filter(id=model_id).delete()
    return JsonResponse({})


def edit(request: WSGIRequest):
    return None

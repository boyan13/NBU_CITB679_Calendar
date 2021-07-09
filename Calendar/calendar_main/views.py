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
        all_events = models.Event.objects.filter(created_by_id=request.user.id)
        data = json.loads(request.body)
        events = data['events']

        try:
            valid_ids = [ev['id'] for ev in events]
            for ev in all_events:
                if ev.id not in valid_ids:
                    ev.delete()

            to_update = []
            to_create = []

            for event in events:
                model = models.Event(
                    title=event["title"],
                    start_date=event["start"],
                    end_date=None if (event["allDay"] is True) else event["end"],
                    created_by=request.user,
                    created_on=datetime.utcnow()
                )

                if not event["id"]:
                    to_create.append(model)
                else:
                    model.pk = event["id"]
                    to_update.append(model)

            models.Event.objects.bulk_update(to_update, ['title', 'start_date', 'end_date'])
            models.Event.objects.bulk_create(to_create)

        except Exception as exc:
            response["isSuccesful"] = False
            return JsonResponse(response)

    return JsonResponse({})

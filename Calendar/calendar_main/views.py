from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from calendar_main.models import Event
import json
from django.http import HttpResponseNotFound, JsonResponse, response
from django.views.decorators.csrf import csrf_exempt

def calendar(request):
    context={
        'calendar_events': []
    }

    if request.user.is_authenticated:
        current_user = request.user
        events = Event.objects.filter(created_by=current_user.id)
        context={
            'calendar_events': events
        }

    return render(request, "calendar.html", context)

@csrf_exempt
def create(request):
    current_user = request.user
    responseObject = {
        "isSuccessful": False
    }

    if request.method == "POST":
        body = json.loads(request.body)
        try:
            events = []
            event = Event()
            for e in body["events"]:
                event.created_by = current_user.id
                event.title = e['title']
                event.day_of_week = 5
                event.start_time = e['title']
                event.end_time = e['title']
                event.for_date = e['title']
                events.append(event)

            Event.objects.bulk_create(events)

            responseObject["isSuccesful"] = True
        except:
            responseObject["isSuccesful"] = False

            return JsonResponse(responseObject)

    return JsonResponse()

def update(request):
    return
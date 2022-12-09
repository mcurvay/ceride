from django.shortcuts import render

from .models import Event, EventStep

def index(request):
    events = Event.objects.all()
    context = {
        'events': events,
    }
    return render(request, 'app/index.html', context)

def detail(request, event_id):
    event = Event.objects.get(id=event_id)
    steps = EventStep.objects.filter(event=event)
    context = {
        'event': event,
        'steps': steps,
    }
    return render(request, 'app/detail.html', context)
from django.http import Http404
from django.views.generic import ListView, DetailView

from .models import Event, Step

# TODO: index sayfası için arama formu eklenecek.
# TODO: index sayfası için filtreleme formu eklenecek.
# TODO: 404 sayfası eklenecek.

class EventListView(ListView):    
    model = Event
    template_name = 'index.html'
    context_object_name = 'events'
    ordering = ['-dateTime']
    paginate_by = 10

    def get_object(self, queryset=None):        
        obj = super().get_object(queryset)
        if obj is None:
            raise Http404("Event does not exist")
        return obj

class EventDetailView(DetailView):
    model = Event
    template_name = 'detail.html'
    context_object_name = 'event'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj is None:
            raise Http404("Event does not exist")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['steps'] = Step.objects.filter(event=self.object)
        return context

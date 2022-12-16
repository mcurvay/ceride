from django.views.generic import ListView, DetailView
from django.db.models import Q

from .models import Event, Step


# TODO: index sayfası için filtreleme formu eklenecek.
# TODO: 404 sayfası eklenecek.

class EventListView(ListView):
    model = Event
    template_name = 'index.html'
    context_object_name = 'events'
    ordering = ['-dateTime']
    paginate_by = 12

    def get_queryset(self):
        query = self.request.GET.get('ara')
        if query is None:
            return Event.objects.all()
        return Event.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )


class EventDetailView(DetailView):
    model = Event
    template_name = 'detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['steps'] = Step.objects.filter(event=self.object)
        return context

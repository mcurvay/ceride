from django.shortcuts import render
from django.views.generic import ListView, DetailView, View

from .filters import EventFilter
from .models import Event, Step


# TODO: Çözüldü, çözülmedi, son 7 gün, son 30 gün gibi filtreleme seçenekleri
# TODO: sayfa yenilendiğinde tüm filtreleme seçim datası gidiyor. Kalsa iyi olur
# TODO: filtre kolayca resetlenmeli
# TODO: 404 sayfası eklenecek.

class EventListView(ListView):
    model = Event
    template_name = 'index.html'
    context_object_name = 'events'
    ordering = ['-dateTime']
    paginate_by = 12

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = EventFilter(self.request.GET, queryset=self.get_queryset())
        return context


class EventDetailView(DetailView):
    model = Event
    template_name = 'detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['steps'] = Step.objects.filter(event=self.object)
        return context


class ChangeLogView(View):
    template_name = 'changelog.html'

    def get(self, request):
        return render(request, self.template_name)


from datetime import datetime
from django.http import Http404, HttpResponse
from django.views.generic import ListView, DetailView, View
from .utils import render_to_pdf

from .models import Event, Step

# TODO: index sayfası için arama formu eklenecek.
# TODO: index sayfası için filtreleme formu eklenecek.
# TODO: detail sayfası için PDF çıktı düğmesi eklenecek.
# TODO: 404 sayfası eklenecek.

class EventListView(ListView):    
    model = Event
    template_name = 'index.html'
    context_object_name = 'events'
    ordering = ['-dateTime']

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

class GeneratePDF(View):
    model = Event
    context_object_name = 'event'

    
    
    def get(self, request, *args, **kwargs):
        data = {
            'id': self.kwargs['pk'],
            'event': Event.objects.get(id=self.kwargs['pk']),
            'steps': Step.objects.filter(event=self.kwargs['pk']),
            'today': datetime.now(),
            }
        pdf = render_to_pdf('report.html', data)
        if pdf:
            response=HttpResponse(pdf,content_type='application/pdf')
            filename = "Report_for_%s.pdf" %(data['id'])
            content = "inline; filename= %s" %(filename)
            response['Content-Disposition']=content
            return response
        return HttpResponse("Page Not Found")

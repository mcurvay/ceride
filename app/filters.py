from django.db.models import Q
from django_filters import FilterSet, CharFilter

from app.models import Event


class EventFilter(FilterSet):
    search = CharFilter(method='search_filter')

    class Meta:
        model = Event
        fields = ['search', 'level', 'type', 'detection_method', 'failure_source', 'solution_by']

    @staticmethod
    def search_filter(queryset, name, value):
        return queryset.filter(Q(title__icontains=value) | Q(description__icontains=value))

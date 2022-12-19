from django.urls import path

from .views import EventDetailView, EventListView, ChangeLogView

app_name = 'app'
urlpatterns = [
    path('', EventListView.as_view(), name='event_list'),
    path('<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('changelog/', ChangeLogView.as_view(), name='changelog')
]

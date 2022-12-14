from django.urls import path

from . import views

app_name = 'app'
urlpatterns = [
    path('', views.EventListView.as_view(), name='event_list'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('<int:pk>/pdf', views.GeneratePDF.as_view(), name='pdf'),
]
"""
URL-Konfiguration für Location-App.
"""
from django.urls import path
from apps.locations import views

app_name = 'locations'

urlpatterns = [
    path('', views.LocationListView.as_view(), name='list'),
    path('<int:pk>/', views.LocationDetailView.as_view(), name='detail'),
    path('create/', views.LocationCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.LocationUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.LocationDeleteView.as_view(), name='delete'),
]


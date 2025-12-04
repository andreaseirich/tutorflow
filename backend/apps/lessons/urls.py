"""
URL-Konfiguration für Lesson-App.
"""
from django.urls import path
from apps.lessons import views

app_name = 'lessons'

urlpatterns = [
    path('', views.LessonListView.as_view(), name='list'),
    path('<int:pk>/', views.LessonDetailView.as_view(), name='detail'),
    path('create/', views.LessonCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.LessonUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.LessonDeleteView.as_view(), name='delete'),
    path('month/<int:year>/<int:month>/', views.LessonMonthView.as_view(), name='month'),
]


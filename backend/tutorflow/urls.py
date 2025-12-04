"""
URL configuration for tutorflow project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('students/', include('apps.students.urls')),
    path('contracts/', include('apps.contracts.urls')),
    path('lessons/', include('apps.lessons.urls')),
    path('blocked-times/', include('apps.blocked_times.urls')),
    path('locations/', include('apps.locations.urls')),
    path('ai/', include('apps.ai.urls')),
]

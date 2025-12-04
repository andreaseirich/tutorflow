from django.contrib import admin
from .models import Lesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['contract', 'date', 'start_time', 'duration_minutes', 'status', 'location']
    search_fields = ['contract__student__first_name', 'contract__student__last_name']
    list_filter = ['status', 'date', 'contract__institute']
    raw_id_fields = ['contract', 'location']
    date_hierarchy = 'date'

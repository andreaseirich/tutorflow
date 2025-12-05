from django.contrib import admin
from .models import Lesson
from .recurring_models import RecurringLesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['contract', 'date', 'start_time', 'duration_minutes', 'status']
    search_fields = ['contract__student__first_name', 'contract__student__last_name']
    list_filter = ['status', 'date', 'contract__institute']
    raw_id_fields = ['contract']
    date_hierarchy = 'date'


@admin.register(RecurringLesson)
class RecurringLessonAdmin(admin.ModelAdmin):
    list_display = ['contract', 'get_weekdays_display', 'start_time', 'start_date', 'is_active']
    search_fields = ['contract__student__first_name', 'contract__student__last_name']
    list_filter = ['is_active', 'start_date', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    raw_id_fields = ['contract']
    date_hierarchy = 'start_date'
    
    def get_weekdays_display(self, obj):
        return obj.get_active_weekdays_display()
    get_weekdays_display.short_description = 'Wochentage'

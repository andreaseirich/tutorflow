from django.contrib import admin

from .models import LessonPlan


@admin.register(LessonPlan)
class LessonPlanAdmin(admin.ModelAdmin):
    list_display = ["student", "topic", "subject", "grade_level", "created_at"]
    search_fields = ["student__first_name", "student__last_name", "topic", "subject"]
    list_filter = ["subject", "grade_level", "created_at"]
    raw_id_fields = ["student", "lesson"]
    date_hierarchy = "created_at"

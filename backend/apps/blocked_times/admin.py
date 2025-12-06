from django.contrib import admin

from .models import BlockedTime


@admin.register(BlockedTime)
class BlockedTimeAdmin(admin.ModelAdmin):
    list_display = ["title", "start_datetime", "end_datetime", "is_recurring", "created_at"]
    search_fields = ["title", "description"]
    list_filter = ["is_recurring", "start_datetime"]
    date_hierarchy = "start_datetime"

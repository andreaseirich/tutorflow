from django.contrib import admin
from .models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'latitude', 'longitude', 'created_at']
    search_fields = ['name', 'address']
    list_filter = ['created_at']

from django.contrib import admin
from .models import Contract


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ['student', 'institute', 'hourly_rate', 'start_date', 'end_date', 'is_active']
    search_fields = ['student__first_name', 'student__last_name', 'institute']
    list_filter = ['is_active', 'start_date', 'institute']
    raw_id_fields = ['student']
    date_hierarchy = 'start_date'

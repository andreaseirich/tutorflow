from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'school', 'grade', 'default_location', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'school']
    list_filter = ['school', 'grade', 'created_at']
    raw_id_fields = ['default_location']

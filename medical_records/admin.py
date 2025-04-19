"""
Admin configuration for medical records application.
Registers models for Django admin interface management.
"""
from django.contrib import admin
from .models import MedicalRecord, Category, Reminder  # PascalCase for class names (correct)


# Constants for admin customization if needed
RECORDS_PER_PAGE = 25
LIST_FILTER_FIELDS = ['record_type', 'date_created']  # snake_case for constants


class MedicalRecordAdmin(admin.ModelAdmin):  # PascalCase for class name (correct)
    """Admin configuration for MedicalRecord model."""
    list_display = ['title', 'user', 'record_type', 'date_created']  # snake_case for variables
    list_filter = LIST_FILTER_FIELDS
    search_fields = ['title', 'description']
    list_per_page = RECORDS_PER_PAGE


class CategoryAdmin(admin.ModelAdmin):  # PascalCase for class name (correct)
    """Admin configuration for Category model."""
    list_display = ['name']
    search_fields = ['name']


class ReminderAdmin(admin.ModelAdmin):  # PascalCase for class name (correct)
    """Admin configuration for Reminder model."""
    list_display = ['medical_record', 'user', 'reminder_date']  # snake_case for variables
    list_filter = ['reminder_date']
    search_fields = ['medical_record__title']


# Register models with their respective admin classes
admin.site.register(MedicalRecord, MedicalRecordAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Reminder, ReminderAdmin)
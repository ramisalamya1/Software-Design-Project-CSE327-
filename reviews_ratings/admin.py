"""
Admin configuration for the reviews and ratings application.
Registers Review and ReviewFlag models for admin interface management.
"""

from django.contrib import admin
from .models import Review, ReviewFlag


class ReviewAdmin(admin.ModelAdmin):
    """Admin configuration for Review model."""
    list_display = ('patient_id', 'hospital', 'doctor', 'created_at', 'anonymous')
    list_filter = ('hospital', 'doctor', 'anonymous', 'created_at')
    search_fields = ('patient_id', 'text', 'hospital__name', 'doctor__name')
    readonly_fields = ('created_at',)


class ReviewFlagAdmin(admin.ModelAdmin):
    """Admin configuration for ReviewFlag model."""
    list_display = ('review', 'reported_by', 'reported_at')
    list_filter = ('reported_at',)
    search_fields = ('reason', 'review__text')
    readonly_fields = ('reported_at',)


admin.site.register(Review, ReviewAdmin)
admin.site.register(ReviewFlag, ReviewFlagAdmin)
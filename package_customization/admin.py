"""
Admin configuration for the package_customization app.
Registers all models to Django admin site.
"""

from django.contrib import admin
from .models import (
    MedicalPackage,
    Accommodation,
    Transport,
    TravelAssistance,
    DietaryOption,
    RehabilitationService
)

# Register models to the admin interface
admin.site.register(MedicalPackage)
admin.site.register(Accommodation)
admin.site.register(Transport)
admin.site.register(TravelAssistance)
admin.site.register(DietaryOption)
admin.site.register(RehabilitationService)
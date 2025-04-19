from django.contrib import admin
from .models import MedicalRecord, Category, Reminder

# Register models for the Django admin interface
# This enables CRUD operations through the admin panel

# Register MedicalRecord model for admin management
admin.site.register(MedicalRecord)

# Register Category model for admin management
admin.site.register(Category)

# Register Reminder model for admin management
admin.site.register(Reminder)
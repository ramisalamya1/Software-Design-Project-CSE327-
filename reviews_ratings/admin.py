"""
Admin configuration for the reviews_ratings application.
This module registers the Review and ReviewFlag models with the Django admin interface,
allowing administrators to manage reviews and flags through the admin panel.
"""
from django.contrib import admin
from .models import Review, ReviewFlag

# Register both Review and ReviewFlag models with default admin interface
admin.site.register([Review, ReviewFlag])
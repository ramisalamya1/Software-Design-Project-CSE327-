"""
Application configuration for the reviews_ratings app.
Defines basic app settings and configurations.
"""

from django.apps import AppConfig

class ReviewsRatingsConfig(AppConfig):
    """Configuration class for the reviews_ratings application"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reviews_ratings'
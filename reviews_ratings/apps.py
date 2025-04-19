from django.apps import AppConfig


class ReviewsRatingsConfig(AppConfig):
    """
    Django app configuration for the reviews and ratings system.
    
    This app handles hospital and doctor reviews, including ratings
    across multiple criteria and review flagging functionality.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reviews_ratings'
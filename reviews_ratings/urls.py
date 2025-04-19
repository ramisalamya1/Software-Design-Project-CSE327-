"""
URL configuration for the reviews_ratings application.
Defines URL patterns for review-related views.
"""

from django.urls import path
from . import views

# URL patterns for review operations
urlpatterns = [
    path('add/', views.add_review, name='add_review'),           # Add new review
    path('edit/<int:pk>/', views.edit_review, name='edit_review'),  # Edit existing review
    path('delete/<int:pk>/', views.delete_review, name='delete_review'),  # Delete review
    path('flag/<int:pk>/', views.flag_review, name='flag_review'),  # Flag inappropriate review
    path('', views.view_reviews, name='view_reviews'),  # List all reviews
]
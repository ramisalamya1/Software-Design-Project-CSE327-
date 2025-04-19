# reviews/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_review, name='add_review'),
    path('edit/<int:pk>/', views.edit_review, name='edit_review'),
    path('delete/<int:pk>/', views.delete_review, name='delete_review'),
    path('flag/<int:pk>/', views.flag_review, name='flag_review'),
    path('', views.view_reviews, name='view_reviews'),
]
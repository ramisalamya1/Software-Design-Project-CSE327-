"""
URL configuration for medical records application.
Defines routing patterns for views and sets application namespace.
"""
from django.urls import path
from django.shortcuts import render
from . import views


# Constants for URL patterns
APP_NAMESPACE = 'medical_records'
HOME_TEMPLATE = 'home.html'


def medical_home(request):  # snake_case for function name
    """Render the medical records home page."""
    return render(request, HOME_TEMPLATE)


# Application namespace
app_name = APP_NAMESPACE  # snake_case for variable name

# URL patterns grouped by functionality
urlpatterns = [
    # Authentication URLs
    path(
        'register/',
        views.register,
        name='register'
    ),
    path(
        'login/',
        views.login_view,  # snake_case for view name
        name='login'
    ),
    path(
        'logout/',
        views.logout_view,  # snake_case for view name
        name='logout'
    ),
    
    # Core application URLs
    path(
        '',
        medical_home,  # snake_case for view name
        name='medical_home'
    ),
    path(
        'upload/',
        views.upload_record,  # snake_case for view name
        name='upload_record'
    ),
    path(
        'view/',
        views.view_records,  # snake_case for view name
        name='view_records'
    ),
    
    # Record sharing and access URLs
    path(
        'share/<int:record_id>/',
        views.share_record,  # snake_case for view name
        name='share_record'
    ),
    path(
        'shared/<str:token>/',
        views.view_shared_record,  # snake_case for view name
        name='view_shared_record'
    ),
    
    # Record download URL
    path(
        'download_record/<int:record_id>/',
        views.download_record,  # snake_case for view name
        name='download_record'
    ),
]
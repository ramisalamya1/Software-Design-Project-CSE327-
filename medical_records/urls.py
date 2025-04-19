from django.urls import path
from django.shortcuts import render
from . import views

# Namespace for the medical records app
app_name = 'medical_records'

def medical_home(request):
    """Render the medical records home page."""
    return render(request, 'home.html')

# URL patterns for the medical records application
urlpatterns = [
    # Authentication URLs
    path('register/', views.register, name='register'),  # User registration
    path('login/', views.login_view, name='login'),     # User login
    path('logout/', views.logout_view, name='logout'),  # User logout
    
    # Core application URLs
    path('', medical_home, name='medical_home'),        # Home page
    path('upload/', views.upload_record, name='upload_record'),  # Upload new records
    path('view/', views.view_records, name='view_records'),      # View all records
    
    # Record sharing and access URLs
    path('share/<int:record_id>/', views.share_record, name='share_record'),  # Share specific record
    path('shared/<str:token>/', views.view_shared_record, name='view_shared_record'),  # Access shared record
    
    # Record download URL
    path('download_record/<int:record_id>/', views.download_record, name='download_record'),  # Download specific record
]
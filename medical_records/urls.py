# medical_records/urls.py

from django.urls import path
from . import views  # Import views

urlpatterns = [
    path('', views.index, name='index'),  # Home page
    path('upload/', views.upload_record, name='upload_record'),
    path('record/<int:record_id>/', views.share_record, name='record_detail'),  # Assuming you meant to use share_record for details
    path('record/<int:record_id>/download/', views.download_pdf, name='download_record_pdf'),  # Fixed the view function to download_pdf
    path('reminder/set/', views.set_reminder, name='set_reminder'),
    path('dashboard/', views.dashboard, name='dashboard'),
]

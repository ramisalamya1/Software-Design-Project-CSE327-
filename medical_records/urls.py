from django.urls import path
from django.shortcuts import render
from . import views

app_name = 'medical_records'

def medical_home(request):
    # Render a global template from the main project directory
    return render(request, 'home.html')  # Assuming home.html is your global template

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', medical_home, name='medical_home'),  # This will handle 'medical/' route
    path('upload/', views.upload_record, name='upload_record'),
    path('view/', views.view_records, name='view_records'),
    path('share/<int:record_id>/', views.share_record, name='share_record'),
    path('download_pdf/<int:record_id>/', views.download_pdf, name='download_pdf'),
]

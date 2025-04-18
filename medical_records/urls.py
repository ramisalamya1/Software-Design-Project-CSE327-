from django.urls import path
from django.shortcuts import render
from . import views

app_name = 'medical_records'

def medical_home(request):
    return render(request, 'home.html')

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', medical_home, name='medical_home'),
    path('upload/', views.upload_record, name='upload_record'),
    path('view/', views.view_records, name='view_records'),
    path('share/<int:record_id>/', views.share_record, name='share_record'),
    path('shared/<str:token>/', views.view_shared_record, name='view_shared_record'),  
    path('download_record/<int:record_id>/', views.download_record, name='download_record'),
]
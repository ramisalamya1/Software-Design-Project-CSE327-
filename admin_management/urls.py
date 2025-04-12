from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('pending-providers/', views.pending_providers, name='pending_providers'),
    path('approve-provider/<int:provider_id>/', views.approve_provider, name='approve_provider'),
    path('suspend-user/<int:user_id>/', views.suspend_user, name='suspend_user'),
]

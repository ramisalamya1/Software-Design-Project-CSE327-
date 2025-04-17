from django.urls import path
from . import views

app_name = 'secure_payment'

urlpatterns = [
    path('payment/<int:package_id>/', views.payment_view, name='payment'),
    path('confirmation/<int:payment_id>/', views.payment_confirmation, name='payment_confirmation'),
    path('refund/<int:payment_id>/', views.refund_request, name='refund_request'),
]

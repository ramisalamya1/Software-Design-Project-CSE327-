from django.contrib import admin
from .models import Payment, Refund

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'package', 'amount', 'currency', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'currency')
    search_fields = ('transaction_id', 'package__hospital__name')
    date_hierarchy = 'created_at'

@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ('id', 'payment', 'amount', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('payment__transaction_id', 'reason')
    date_hierarchy = 'created_at'
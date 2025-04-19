from django.contrib import admin
from .models import Payment, Refund

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Payment model.
    
    This class defines how the Payment model is displayed in the Django admin interface.
    
    Attributes:
        list_display: Specifies which fields to display in the list view.
        list_filter: Adds filter options for specific fields.
        search_fields: Enables search functionality for specific fields.
        date_hierarchy: Adds a date-based navigation for filtering records by date.
    """
    list_display = ('id', 'package', 'amount', 'currency', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'currency')
    search_fields = ('transaction_id', 'package__hospital__name')
    date_hierarchy = 'created_at'

@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Refund model.
    
    This class defines how the Refund model is displayed in the Django admin interface.
    
    Attributes:
        list_display: Specifies which fields to display in the list view.
        list_filter: Adds filter options for specific fields.
        search_fields: Enables search functionality for specific fields.
        date_hierarchy: Adds a date-based navigation for filtering records by date.
    """
    list_display = ('id', 'payment', 'amount', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('payment__transaction_id', 'reason')
    date_hierarchy = 'created_at'

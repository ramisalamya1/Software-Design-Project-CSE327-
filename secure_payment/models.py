from django.db import models
from package_customization.models import MedicalPackage
from django.core.validators import MinValueValidator

class Payment(models.Model):
    """
    Model for handling payment information and tracking.
    
    This model stores details about payments, including status, amount, payment method, 
    transaction ID, and installment information. It also tracks timestamps for the creation 
    and update of each payment entry.
    
    Attributes:
        PAYMENT_STATUS_CHOICES: A list of possible payment statuses.
        PAYMENT_METHOD_CHOICES: A list of accepted payment methods.
        CURRENCY_CHOICES: A list of supported currencies.
        package: A foreign key to the MedicalPackage model, linking the payment to a specific package.
        amount: The total amount of the payment.
        currency: The currency of the payment (USD, EUR, GBP, INR).
        payment_method: The method used for the payment (credit_card, bank_transfer, etc.).
        status: The current status of the payment (pending, completed, etc.).
        transaction_id: A unique identifier for the transaction.
        created_at: The date and time when the payment was created.
        updated_at: The date and time when the payment was last updated.
        is_installment: A flag indicating if the payment is an installment.
        installment_count: The number of installments if the payment is split.
    """
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded')
    ]

    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('paypal', 'PayPal'),
        ('google_pay', 'Google Pay'),
        ('apple_pay', 'Apple Pay')
    ]

    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
        ('INR', 'Indian Rupee')
    ]

    package = models.ForeignKey(MedicalPackage, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_installment = models.BooleanField(default=False)
    installment_count = models.IntegerField(default=1)

    def __str__(self):
        """
        String representation of the Payment model.

        Returns:
            str: A string representing the payment ID, package, and payment status.
        """
        return f"Payment {self.id} - {self.package} - {self.status}"

class Refund(models.Model):
    """
    Model for handling refund requests and tracking.
    
    This model stores details about refund requests associated with payments, 
    including the amount refunded, the reason, and the refund status.
    
    Attributes:
        REFUND_STATUS_CHOICES: A list of possible refund statuses.
        payment: A foreign key to the Payment model, linking the refund to a specific payment.
        amount: The total amount of the refund.
        reason: The reason for the refund request.
        status: The current status of the refund request.
        created_at: The date and time when the refund was created.
        updated_at: The date and time when the refund was last updated.
    """
    
    REFUND_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed')
    ]

    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='refunds')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=REFUND_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        String representation of the Refund model.

        Returns:
            str: A string representing the refund ID, associated payment, and refund status.
        """
        return f"Refund {self.id} - {self.payment} - {self.status}"

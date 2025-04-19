from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Payment, Refund
from package_customization.models import MedicalPackage  # Updated import
from decimal import Decimal
import uuid

def payment_view(request, package_id):
    """
    View to handle payment processing for a selected package.
    
    This view allows users to choose a payment method, currency, and installment options.
    It creates a new payment record and processes the payment. In a real-world scenario,
    this is where the integration with a payment gateway would occur.
    
    Args:
        request: The HTTP request object containing form data and other request-related information.
        package_id: The ID of the MedicalPackage for which the payment is being processed.
    
    Returns:
        Rendered template for the payment page or redirect to payment confirmation page.
    
    Raises:
        Http404: If the specified MedicalPackage does not exist.
    """
    package = get_object_or_404(MedicalPackage, id=package_id)
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        currency = request.POST.get('currency')
        is_installment = request.POST.get('is_installment') == 'on'
        installment_count = int(request.POST.get('installment_count', 1))
        
        # Create payment record
        payment = Payment.objects.create(
            package=package,
            amount=package.total_cost,
            currency=currency,
            payment_method=payment_method,
            transaction_id=str(uuid.uuid4()),
            is_installment=is_installment,
            installment_count=installment_count
        )
        
        # Mark payment as completed (demo purpose)
        payment.status = 'completed'
        payment.save()
        
        messages.success(request, 'Payment processed successfully!')
        return redirect('payment_confirmation', payment_id=payment.id)
    
    return render(request, 'secure_payment/payment.html', {
        'package': package,
        'payment_methods': Payment.PAYMENT_METHOD_CHOICES,
        'currencies': Payment.CURRENCY_CHOICES
    })

def payment_confirmation(request, payment_id):
    """
    View to display payment confirmation details.
    
    This view shows the confirmation page after a successful payment has been processed. 
    It retrieves the payment details and renders the confirmation page.
    
    Args:
        request: The HTTP request object.
        payment_id: The ID of the Payment record for which the confirmation is displayed.
    
    Returns:
        Rendered template for the payment confirmation page.
    
    Raises:
        Http404: If the specified Payment does not exist.
    """
    payment = get_object_or_404(Payment, id=payment_id)
    return render(request, 'secure_payment/confirmation.html', {'payment': payment})

def refund_request(request, payment_id):
    """
    View to handle refund requests.
    
    This view allows users to request a refund for a payment. It creates a Refund record
    associated with the original Payment. The refund request can be processed after submission.
    
    Args:
        request: The HTTP request object containing the reason for the refund.
        payment_id: The ID of the Payment for which the refund is being requested.
    
    Returns:
        Rendered template for the refund request page or redirect to payment confirmation page.
    
    Raises:
        Http404: If the specified Payment does not exist.
    """
    payment = get_object_or_404(Payment, id=payment_id)
    
    if request.method == 'POST':
        reason = request.POST.get('reason')
        refund = Refund.objects.create(
            payment=payment,
            amount=payment.amount,
            reason=reason
        )
        messages.success(request, 'Refund request submitted successfully!')
        return redirect('payment_confirmation', payment_id=payment.id)
    
    return render(request, 'secure_payment/refund.html', {'payment': payment})

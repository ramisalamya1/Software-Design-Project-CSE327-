from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Payment, Refund
from package_customization.models import MedicalPackage  # Updated import
from decimal import Decimal
import uuid

def payment_view(request, package_id):
    """
    View to handle payment processing for a selected package.
    """
    package = get_object_or_404(MedicalPackage, id=package_id)  # Updated model name
    
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
        
        # In a real application, you would integrate with a payment gateway here
        # For demo purposes, we'll just mark it as completed
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
    """
    payment = get_object_or_404(Payment, id=payment_id)
    return render(request, 'secure_payment/confirmation.html', {'payment': payment})

def refund_request(request, payment_id):
    """
    View to handle refund requests.
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

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Patient

# Create your views here.
# def booking(request):
#     return render(request, "appointment_booking.html")
    
def book_appointment(request):
    if request.method == 'POST':
        form = Patient(request.POST)
        if form.is_valid():
            appointment = form.save()
            # todo pass appointment ID via session or URL for payment
            return redirect('payment_redirect', appointment_id=appointment.id)
    else:
        form = Patient()
    return render(request, "appointment_booking.html")
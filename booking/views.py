from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Patient
from hospital_search.models import Hospital


# Create your views here.
# def booking(request):
#     return render(request, "appointment_booking.html")
    
def book_appointment(request, hospital_id):
    """
    Handles the appointment booking process for a selected hospital.

    Retrieves the hospital by ID, displays the appointment form, and processes the submitted form.

    Args:
        request (HttpRequest): The incoming HTTP request.
        hospital_id (int): The ID of the hospital for which the appointment is being booked.

    Returns:
        HttpResponse: Renders the appointment form template or redirects to the payment page after booking.
    """
    hospital = get_object_or_404(Hospital, pk=hospital_id)

    if request.method == 'POST':
        form = Patient(request.POST)
        if form.is_valid():
            appointment = form.save()
            # todo pass appointment ID via session or URL for payment
            return redirect('payment_redirect', appointment_id=appointment.id)
    else:
        form = Patient()
    return render(request, 'appointment_booking.html', {'hospital': hospital})
"""
Views for package customization.
Handles rendering and saving medical travel packages.
"""

from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import (
    MedicalPackage,
    Accommodation,
    Transport,
    TravelAssistance,
    DietaryOption,
    RehabilitationService,
    Hospital
)
import json


def package_customization_view(request):
    """
    Renders the package customization form page with all available services.
    """
    hospitals = Hospital.objects.all()
    accommodations = Accommodation.objects.filter(available=True)
    transports = Transport.objects.filter(available=True)
    travel_assistance = TravelAssistance.objects.all()
    dietary_options = DietaryOption.objects.filter(available=True)
    rehab_services = RehabilitationService.objects.all()

    context = {
        'hospitals': hospitals,
        'accommodations': accommodations,
        'transports': transports,
        'travel_assistance': travel_assistance,
        'dietary_options': dietary_options,
        'rehab_services': rehab_services,
    }

    return render(request, 'package_customization/customize.html', context)




@csrf_exempt
def save_package(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Create the package
            package = MedicalPackage.objects.create(
                user_name=data['user_name'],
                hospital_id=data['hospital'],
                treatment_date=data['treatment_date'],
                accommodation_id=data.get('accommodation'),
                transport_id=data.get('transport'),
                dietary_option_id=data.get('dietary_option'),
                rehabilitation_id=data.get('rehabilitation'),
                total_cost=data['total_cost'],
                notes=data.get('notes', '')
            )

            if 'travel_assistance' in data:
                package.travel_assistance.set(data['travel_assistance'])

            # Generate the correct URL using reverse()
            redirect_url = reverse('secure_payment:payment', kwargs={'package_id': package.id})
            
            return JsonResponse({
                'status': 'success',
                'message': 'Package saved successfully',
                'package_id': package.id,
                'redirect_url': redirect_url
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)
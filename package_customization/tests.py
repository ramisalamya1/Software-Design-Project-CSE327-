from django.test import TestCase, Client
from django.urls import reverse
from datetime import date
import json

from .models import (
    Hospital, Accommodation, Transport,
    TravelAssistance, DietaryOption,
    RehabilitationService, MedicalPackage
)


class PackageCustomizationTest(TestCase):
    """
    Unit tests for package_customization app:
    - Model creation
    - API POST view
    """

    def setUp(self):
        """Set up sample data for all models."""
        self.hospital = Hospital.objects.create(
            name="Test Hospital",
            city="Test City",
            country="Testland",
            treatment_type="General",
            cost_estimate=1000
        )

        self.accommodation = Accommodation.objects.create(
            name="Test Hotel",
            type="Hotel",
            distance_to_hospital=2.5,
            cost_per_night=120.00,
            amenities="WiFi, AC",
            available=True
        )

        self.transport = Transport.objects.create(
            type="Private Car",
            provider="Test Travels",
            cost_per_km=15.00,
            available=True
        )

        self.dietary_option = DietaryOption.objects.create(
            name="Vegetarian",
            description="Plant-based meals",
            cost_per_day=25.00,
            available=True
        )

        self.rehabilitation = RehabilitationService.objects.create(
            name="Rehab Center",
            type="Physiotherapy",
            provider="HealthPlus",
            cost_per_session=50.00,
            duration=45
        )

        self.travel_assist = TravelAssistance.objects.create(
            service_type="Visa Support",
            provider="Assist Co.",
            cost=80.00,
            description="Help with medical visa"
        )

    def test_medical_package_creation(self):
        """Test creation of a medical package instance."""
        package = MedicalPackage.objects.create(
            user_name="John Doe",
            hospital=self.hospital,
            treatment_date=date.today(),
            accommodation=self.accommodation,
            transport=self.transport,
            dietary_option=self.dietary_option,
            rehabilitation=self.rehabilitation,
            total_cost=1000.00,
            notes="Test note"
        )
        package.travel_assistance.add(self.travel_assist)

        self.assertEqual(package.user_name, "John Doe")
        self.assertEqual(str(package), f"Package for John Doe at {self.hospital.name}")

    def test_save_package_post_api(self):
        """Test POST request to save_package view."""
        client = Client()

        payload = {
            "user_name": "Jane Doe",
            "hospital": self.hospital.id,
            "treatment_date": str(date.today()),
            "accommodation": self.accommodation.id,
            "transport": self.transport.id,
            "dietary_option": self.dietary_option.id,
            "rehabilitation": self.rehabilitation.id,
            "total_cost": "1500.00",
            "notes": "Test API note",
            "travel_assistance": [self.travel_assist.id]
        }

        response = client.post(
            reverse('package_customization:save_package'),
            data=json.dumps(payload),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.json()["status"])
        self.assertTrue(MedicalPackage.objects.filter(user_name="Jane Doe").exists())

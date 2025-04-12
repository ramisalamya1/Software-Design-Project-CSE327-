"""
Unit tests for the Hospital Comparison feature.

These tests validate that the view:
- returns correct status
- compares hospitals properly
- highlights the best recommendation
- handles edge cases gracefully
"""

from django.test import TestCase
from django.urls import reverse
from hospital_search.models import Hospital
from hospital_comparison.models import HospitalStats


class HospitalComparisonTests(TestCase):
    """
    Test suite for the hospital_comparison view and logic.
    """

    def setUp(self):
        """
        Create test hospitals and stats before each test.
        """
        self.h1 = Hospital.objects.create(
            name="Apollo Hospital",
            city="Delhi",
            country="India",
            treatment_type="Surgery",
            accreditation="NABH",
            cost_estimate=1500.00,
            accepts_insurance=True,
            is_available=True
        )

        self.h2 = Hospital.objects.create(
            name="Fortis Healthcare",
            city="Mumbai",
            country="India",
            treatment_type="Cardiology",
            accreditation="JCI",
            cost_estimate=2500.00,
            accepts_insurance=True,
            is_available=True
        )

        self.h3 = Hospital.objects.create(
            name="AIIMS",
            city="Delhi",
            country="India",
            treatment_type="Neurology",
            accreditation="NABH",
            cost_estimate=1000.00,
            accepts_insurance=True,
            is_available=True
        )

        HospitalStats.objects.create(
            hospital=self.h1,
            recovery_rate=95.5,
            icu_capacity=50,
            has_robotic_surgery=True,
            medical_equipment="MRI, CT Scan",
            post_treatment_support="24/7",
            accreditation="NABH"
        )

        HospitalStats.objects.create(
            hospital=self.h2,
            recovery_rate=92.0,
            icu_capacity=45,
            has_robotic_surgery=True,
            medical_equipment="Cardiac unit",
            post_treatment_support="3 months",
            accreditation="JCI"
        )

        HospitalStats.objects.create(
            hospital=self.h3,
            recovery_rate=88.5,
            icu_capacity=60,
            has_robotic_surgery=False,
            medical_equipment="General Equipment",
            post_treatment_support="1 month",
            accreditation="NABH"
        )

    def test_compare_view_status_code(self):
        """
        Ensure the comparison view loads successfully.
        """
        url = reverse("hospital_comparison:compare")
        response = self.client.get(url + "?ids=1,2,3")
        self.assertEqual(response.status_code, 200)

    def test_compare_view_context(self):
        """
        Ensure hospitals and stats_map are present in context.
        """
        response = self.client.get(reverse("hospital_comparison:compare") + "?ids=1,2,3")
        self.assertIn("hospitals", response.context)
        self.assertIn("stats_map", response.context)
        self.assertEqual(len(response.context["hospitals"]), 3)

    def test_best_recommendation_logic(self):
        """
        Ensure the correct hospital is marked as recommended based on score.
        """
        response = self.client.get(reverse("hospital_comparison:compare") + "?ids=1,2,3")
        recommended = response.context["recommended"]
        self.assertEqual(recommended.name, "AIIMS")  


    def test_view_without_ids(self):
        """
        Ensure the view handles missing IDs gracefully.
        """
        response = self.client.get(reverse("hospital_comparison:compare"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No hospitals selected")

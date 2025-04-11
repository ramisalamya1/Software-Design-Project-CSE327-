from django.test import TestCase, Client
from django.urls import reverse
from .models import Hospital

class HospitalSearchTests(TestCase):
    """
    Unit tests for the Hospital Search feature.
    """

    def setUp(self):
        """
        Set up test data for hospital search.
        """
        Hospital.objects.create(
            name="Test Hospital A",
            city="Dhaka",
            country="Bangladesh",
            accreditation="NABH",
            treatment_type="Cardiology",
            cost_estimate=1200.00,
            accepts_insurance=True,
            is_available=True,
        )

        Hospital.objects.create(
            name="Test Hospital B",
            city="Chittagong",
            country="Bangladesh",
            accreditation="JCI",
            treatment_type="Neurology",
            cost_estimate=2000.00,
            accepts_insurance=False,
            is_available=True,
        )

        self.client = Client()

    def test_hospital_list_view_status_code(self):
        """
        Test if the hospital search view returns a 200 status code.
        """
        response = self.client.get(reverse('hospital_search'))
        self.assertEqual(response.status_code, 200)

    def test_filter_by_city(self):
        """
        Test filtering hospitals by city.
        """
        response = self.client.get(reverse('hospital_search'), {'city': 'Dhaka'})
        self.assertContains(response, "Test Hospital A")
        self.assertNotContains(response, "Test Hospital B")

    def test_filter_by_accreditation(self):
        """
        Test filtering hospitals by accreditation.
        """
        response = self.client.get(reverse('hospital_search'), {'accreditation': 'JCI'})
        self.assertContains(response, "Test Hospital B")
        self.assertNotContains(response, "Test Hospital A")

    def test_sort_by_cost_ascending(self):
        """
        Test sorting hospitals by cost in ascending order.
        """
        response = self.client.get(reverse('hospital_search'), {'sort_by': 'cost_asc'})
        hospitals = list(response.context['hospitals'])
        self.assertLessEqual(hospitals[0].cost_estimate, hospitals[1].cost_estimate)

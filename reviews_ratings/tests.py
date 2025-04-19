from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from .models import PatientReview, Hospital, Doctor, ReviewReport
from .forms import PatientReviewForm, ReviewReportForm
from datetime import timedelta


class PatientReviewModelTest(TestCase):
    """Test cases for the PatientReview model functionality."""
    
    def setUp(self):
        """Set up test data for PatientReview model tests."""
        self.test_hospital = Hospital.objects.create(name="Test Hospital")
        self.test_doctor = Doctor.objects.create(name="Dr. Test")

        self.test_review = PatientReview.objects.create(
            hospital=self.test_hospital,
            doctor=self.test_doctor,
            service_quality_rating=4,
            cost_transparency_rating=4,
            facility_standards_rating=4,
            treatment_effectiveness_rating=4,
            review_text="Great service",
            is_anonymous=True,
            patient_id="P123"
        )

    def test_string_representation(self):
        """Test the string representation of a PatientReview."""
        self.assertEqual(str(self.test_review), "Patient review by P123")

    def test_rating_calculation(self):
        """Test the average rating calculation."""
        self.assertEqual(self.test_review.calculate_average_rating(), 4.0)

    def test_review_editable_when_new(self):
        """Test review editability when newly created."""
        self.assertTrue(self.test_review.is_editable)

    def test_review_not_editable_after_timeout(self):
        """Test review editability after time limit."""
        self.test_review.review_date = timezone.now() - timedelta(minutes=61)
        self.test_review.save()
        self.assertFalse(self.test_review.is_editable)


class ReviewReportModelTest(TestCase):
    """Test cases for the ReviewReport model functionality."""

    def setUp(self):
        """Set up test data for ReviewReport model tests."""
        self.test_review = PatientReview.objects.create(
            service_quality_rating=3,
            cost_transparency_rating=3,
            facility_standards_rating=3,
            treatment_effectiveness_rating=3,
            review_text="Needs improvement",
            is_anonymous=False,
        )
        self.test_report = ReviewReport.objects.create(
            reviewed_content=self.test_review,
            report_reason="Inappropriate content"
        )

    def test_string_representation(self):
        """Test the string representation of a ReviewReport."""
        self.assertEqual(str(self.test_report), f"Report for review {self.test_review.id}")


class PatientReviewFormTest(TestCase):
    """Test cases for the PatientReviewForm functionality."""

    def test_form_with_valid_data(self):
        """Test form validation with valid data."""
        test_hospital = Hospital.objects.create(name="Form Hospital")
        test_doctor = Doctor.objects.create(name="Form Doctor")
        form_data = {
            'hospital': test_hospital.id,
            'doctor': test_doctor.id,
            'is_anonymous': True,
            'service_quality_rating': 4,
            'cost_transparency_rating': 4,
            'facility_standards_rating': 4,
            'treatment_effectiveness_rating': 4,
            'review_text': "Nice experience",
            'patient_id': "P456"
        }
        form = PatientReviewForm(data=form_data)
        self.assertTrue(form.is_valid())


class ReviewReportFormTest(TestCase):
    """Test cases for the ReviewReportForm functionality."""

    def test_form_with_valid_data(self):
        """Test report form validation with valid data."""
        form_data = {'report_reason': "Offensive language"}
        form = ReviewReportForm(data=form_data)
        self.assertTrue(form.is_valid())


class PatientReviewViewsTest(TestCase):
    """Test cases for review-related views."""

    def setUp(self):
        """Set up test data for view tests."""
        self.test_client = Client()
        self.test_hospital = Hospital.objects.create(name="Test Hospital")
        self.test_doctor = Doctor.objects.create(name="Test Doctor")
        self.test_review = PatientReview.objects.create(
            hospital=self.test_hospital,
            doctor=self.test_doctor,
            service_quality_rating=5,
            cost_transparency_rating=5,
            facility_standards_rating=5,
            treatment_effectiveness_rating=5,
            review_text="Excellent",
            is_anonymous=False,
            patient_id="TestUser"
        )

    def test_list_reviews(self):
        """Test the review listing view."""
        response = self.test_client.get(reverse('view_reviews'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review_list.html')

    def test_create_review_get(self):
        """Test GET request to create review page."""
        response = self.test_client.get(reverse('add_review'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review_form.html')

    def test_create_review_post(self):
        """Test POST request to create a new review."""
        response = self.test_client.post(reverse('add_review'), {
            'hospital': self.test_hospital.id,
            'doctor': self.test_doctor.id,
            'is_anonymous': False,
            'service_quality_rating': 4,
            'cost_transparency_rating': 4,
            'facility_standards_rating': 4,
            'treatment_effectiveness_rating': 4,
            'review_text': "Good service",
            'patient_id': "P789"
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(PatientReview.objects.count(), 2)

    def test_update_review(self):
        """Test editing an existing review."""
        response = self.test_client.post(reverse('edit_review', args=[self.test_review.pk]), {
            'hospital': self.test_hospital.id,
            'doctor': self.test_doctor.id,
            'is_anonymous': False,
            'service_quality_rating': 3,
            'cost_transparency_rating': 3,
            'facility_standards_rating': 3,
            'treatment_effectiveness_rating': 3,
            'review_text': "Updated review",
            'patient_id': "TestUser"
        })
        self.assertEqual(response.status_code, 302)
        self.test_review.refresh_from_db()
        self.assertEqual(self.test_review.review_text, "Updated review")

    def test_remove_review(self):
        """Test deleting a review."""
        response = self.test_client.get(reverse('delete_review', args=[self.test_review.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(PatientReview.objects.filter(pk=self.test_review.pk).exists())

    def test_report_review_get(self):
        """Test GET request to report review page."""
        response = self.test_client.get(reverse('flag_review', args=[self.test_review.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flag_review.html')

    def test_report_review_post(self):
        """Test POST request to report a review."""
        response = self.test_client.post(reverse('flag_review', args=[self.test_review.pk]), {
            'report_reason': "Spam content"
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ReviewReport.objects.count(), 1)
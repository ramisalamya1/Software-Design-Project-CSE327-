from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from .models import Review, Hospital, Doctor, ReviewFlag
from .forms import ReviewForm, ReviewFlagForm
from datetime import timedelta


class ReviewModelTest(TestCase):
    def setUp(self):
        self.hospital = Hospital.objects.create(name="Test Hospital")
        self.doctor = Doctor.objects.create(name="Dr. Test")

        self.review = Review.objects.create(
            hospital=self.hospital,
            doctor=self.doctor,
            service_quality=4,
            cost_transparency=4,
            facility_standards=4,
            treatment_effectiveness=4,
            text="Great service",
            anonymous=True,
            patient_id="P123"
        )

    def test_str_method(self):
        self.assertEqual(str(self.review), "Review by P123")

    def test_average_rating(self):
        self.assertEqual(self.review.average_rating(), 4.0)

    def test_is_editable_true(self):
        self.assertTrue(self.review.is_editable)

    def test_is_editable_false(self):
        self.review.created_at = timezone.now() - timedelta(minutes=61)
        self.review.save()
        self.assertFalse(self.review.is_editable)


class ReviewFlagModelTest(TestCase):
    def setUp(self):
        self.review = Review.objects.create(
            service_quality=3,
            cost_transparency=3,
            facility_standards=3,
            treatment_effectiveness=3,
            text="Needs improvement",
            anonymous=False,
        )
        self.flag = ReviewFlag.objects.create(
            review=self.review,
            reason="Inappropriate content"
        )

    def test_flag_str_method(self):
        self.assertEqual(str(self.flag), f"Flag on {self.review.id} by Anonymous")


class ReviewFormTest(TestCase):
    def test_valid_review_form(self):
        hospital = Hospital.objects.create(name="Form Hospital")
        doctor = Doctor.objects.create(name="Form Doctor")
        data = {
            'hospital': hospital.id,
            'doctor': doctor.id,
            'anonymous': True,
            'service_quality': 4,
            'cost_transparency': 4,
            'facility_standards': 4,
            'treatment_effectiveness': 4,
            'text': "Nice experience",
            'patient_id': "P456"
        }
        form = ReviewForm(data=data)
        self.assertTrue(form.is_valid())


class ReviewFlagFormTest(TestCase):
    def test_valid_flag_form(self):
        data = {'reason': "Offensive language"}
        form = ReviewFlagForm(data=data)
        self.assertTrue(form.is_valid())


class ReviewViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.hospital = Hospital.objects.create(name="Test Hospital")
        self.doctor = Doctor.objects.create(name="Test Doctor")
        self.review = Review.objects.create(
            hospital=self.hospital,
            doctor=self.doctor,
            service_quality=5,
            cost_transparency=5,
            facility_standards=5,
            treatment_effectiveness=5,
            text="Excellent",
            anonymous=False,
            patient_id="TestUser"
        )

    def test_view_reviews(self):
        response = self.client.get(reverse('view_reviews'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review_list.html')

    def test_add_review_get(self):
        response = self.client.get(reverse('add_review'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review_form.html')

    def test_add_review_post(self):
        response = self.client.post(reverse('add_review'), {
            'hospital': self.hospital.id,
            'doctor': self.doctor.id,
            'anonymous': False,
            'service_quality': 4,
            'cost_transparency': 4,
            'facility_standards': 4,
            'treatment_effectiveness': 4,
            'text': "Good service",
            'patient_id': "P789"
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.count(), 2)

    def test_edit_review(self):
        response = self.client.post(reverse('edit_review', args=[self.review.pk]), {
            'hospital': self.hospital.id,
            'doctor': self.doctor.id,
            'anonymous': False,
            'service_quality': 3,
            'cost_transparency': 3,
            'facility_standards': 3,
            'treatment_effectiveness': 3,
            'text': "Updated review",
            'patient_id': "TestUser"
        })
        self.assertEqual(response.status_code, 302)
        self.review.refresh_from_db()
        self.assertEqual(self.review.text, "Updated review")

    def test_delete_review(self):
        response = self.client.get(reverse('delete_review', args=[self.review.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Review.objects.filter(pk=self.review.pk).exists())

    def test_flag_review_get(self):
        response = self.client.get(reverse('flag_review', args=[self.review.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flag_review.html')

    def test_flag_review_post(self):
        response = self.client.post(reverse('flag_review', args=[self.review.pk]), {
            'reason': "Spam content"
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ReviewFlag.objects.count(), 1)

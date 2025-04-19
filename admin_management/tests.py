from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import CustomUser, ProviderProfile, AdminActionLog
from django.utils import timezone

class CustomUserModelTest(TestCase):
    def test_create_custom_user(self):
        user = CustomUser.objects.create_user(username='testuser', password='password123', role='provider')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.role, 'provider')
        self.assertFalse(user.is_approved)

class ProviderProfileModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='provider1', password='password', role='provider')

    def test_create_provider_profile(self):
        fake_file = SimpleUploadedFile("doc.pdf", b"file_content")
        profile = ProviderProfile.objects.create(
            user=self.user,
            hospital_name='HealthCare Hospital',
            license_number='LIC123456',
            documents=fake_file,
            approved_by_admin=True
        )
        self.assertEqual(profile.user.username, 'provider1')
        self.assertEqual(profile.hospital_name, 'HealthCare Hospital')
        self.assertTrue(profile.approved_by_admin)

class AdminActionLogTest(TestCase):
    def setUp(self):
        self.admin = CustomUser.objects.create_user(username='admin1', password='adminpass', role='admins')

    def test_admin_action_log_creation(self):
        log = AdminActionLog.objects.create(
            admin=self.admin,
            action='Approved provider profile'
        )
        self.assertEqual(log.admin.username, 'admin1')
        self.assertEqual(log.action, 'Approved provider profile')
        self.assertLessEqual(log.timestamp, timezone.now())

# Django imports
from django.apps import AppConfig


class MedicalRecordsConfig(AppConfig):  # PascalCase for class name (correct)
    """
    Configuration class for the medical_records application.
    Follows Django's app configuration standards.
    """
    default_auto_field = 'django.db.models.BigAutoField'  # snake_case for variable name
    name = 'medical_records'  # snake_case for module name (correct)

"""
URL routes for package_customization app.
"""

from django.urls import path
from .views import package_customization_view, save_package

app_name = 'package_customization'

urlpatterns = [
    path('customize/', package_customization_view, name='customize'),
    path('save-package/', save_package, name='save_package'),
]

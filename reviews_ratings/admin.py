# reviews/admin.py

from django.contrib import admin
from .models import Review, ReviewFlag, Hospital, Doctor

admin.site.register([Review, ReviewFlag, Hospital, Doctor])

# reviews/admin.py

from django.contrib import admin
from .models import Review, ReviewFlag


admin.site.register([Review, ReviewFlag])
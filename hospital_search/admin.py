from django.contrib import admin

# Register your models here.

from .models import Hospital, Doctor, Facility, Review

admin.site.register(Hospital)
admin.site.register(Doctor)
admin.site.register(Facility)
admin.site.register(Review)

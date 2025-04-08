from django.contrib import admin
from .models import MedicalRecord, Category, Reminder

admin.site.register(MedicalRecord)
admin.site.register(Category)
admin.site.register(Reminder)

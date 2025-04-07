from django.contrib import admin
from .models import MedicalRecord, RecordVersion, SharedAccess, Reminder

admin.site.register(MedicalRecord)
admin.site.register(RecordVersion)
admin.site.register(SharedAccess)
admin.site.register(Reminder)

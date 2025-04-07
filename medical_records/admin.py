from django.contrib import admin
from .models import MedicalRecord, RecordVersion, Reminder, SharedAccess

# Register your models here.

class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'record_type', 'date', 'created_at', 'updated_at', 'version')
    search_fields = ('title', 'user__username', 'record_type')
    list_filter = ('record_type', 'user')

class RecordVersionAdmin(admin.ModelAdmin):
    list_display = ('record', 'version_number', 'updated_at', 'file')
    search_fields = ('record__title', 'version_number')

class ReminderAdmin(admin.ModelAdmin):
    list_display = ('user', 'record', 'reminder_date', 'message')
    search_fields = ('user__username', 'record__title')
    list_filter = ('reminder_date',)

class SharedAccessAdmin(admin.ModelAdmin):
    list_display = ('record', 'access_token', 'expires_at')
    search_fields = ('record__title', 'access_token')

# Register the models with custom admin classes
admin.site.register(MedicalRecord, MedicalRecordAdmin)
admin.site.register(RecordVersion, RecordVersionAdmin)
admin.site.register(Reminder, ReminderAdmin)
admin.site.register(SharedAccess, SharedAccessAdmin)

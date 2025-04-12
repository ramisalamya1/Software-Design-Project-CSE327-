from django.contrib import admin
from .models import ComparisonRecord, HospitalStats

@admin.register(ComparisonRecord)
class ComparisonRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')
    filter_horizontal = ('selected_hospitals',)

@admin.register(HospitalStats)
class HospitalStatsAdmin(admin.ModelAdmin):
    list_display = ('hospital', 'recovery_rate', 'icu_capacity', 'has_robotic_surgery')
    list_filter = ('has_robotic_surgery', 'accreditation')
    search_fields = ('hospital__name', 'medical_equipment')


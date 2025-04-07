from django.shortcuts import render, redirect, get_object_or_404
from .models import MedicalRecord, Reminder, SharedAccess, RecordVersion
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.http import HttpResponse
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from reportlab.pdfgen import canvas  # type: ignore
import datetime

# View to show the home page or index
def index(request):
    return render(request, 'medical_records/index.html')

# Dashboard view to show records and reminders for the logged-in user
@login_required
def dashboard(request):
    records = MedicalRecord.objects.filter(user=request.user).order_by('-date')
    reminders = Reminder.objects.filter(user=request.user).order_by('reminder_date')
    return render(request, 'medical_records/dashboard.html', {'records': records, 'reminders': reminders})

# View for uploading a new medical record
@login_required
def upload_record(request):
    if request.method == 'POST':
        title = request.POST['title']
        record_type = request.POST['record_type']
        date = request.POST['date']
        note = request.POST.get('note', '')
        file = request.FILES['file']
        record = MedicalRecord.objects.create(
            user=request.user,
            title=title,
            record_type=record_type,
            date=date,
            encrypted_file=file,
            note=note
        )
        return redirect('dashboard')
    return render(request, 'medical_records/upload.html')

# View for sharing a record with a generated link
@login_required
def share_record(request, record_id):
    record = get_object_or_404(MedicalRecord, id=record_id, user=request.user)
    token = get_random_string(32)
    expires = timezone.now() + timezone.timedelta(days=1)
    SharedAccess.objects.create(record=record, access_token=token, expires_at=expires)
    share_link = request.build_absolute_uri(reverse('view_shared', args=[token]))
    return render(request, 'medical_records/share.html', {'link': share_link, 'expires': expires})

# View for viewing a shared record by its token
def view_shared(request, token):
    shared = get_object_or_404(SharedAccess, access_token=token)
    if timezone.now() > shared.expires_at:
        return HttpResponse("Link expired.")
    return render(request, 'medical_records/shared_view.html', {'record': shared.record})

# View for setting a reminder for a specific record
@login_required
def set_reminder(request, record_id):
    if request.method == 'POST':
        date = request.POST['reminder_date']
        message = request.POST['message']
        Reminder.objects.create(user=request.user, record_id=record_id, reminder_date=date, message=message)
        return redirect('dashboard')
    return render(request, 'medical_records/set_reminder.html', {'record_id': record_id})

# View for displaying the details of a specific record
@login_required
def record_detail(request, record_id):
    record = get_object_or_404(MedicalRecord, id=record_id, user=request.user)
    return render(request, 'medical_records/record_detail.html', {'record': record})

# View for downloading a record as a PDF
@login_required
def download_pdf(request, record_id):
    record = get_object_or_404(MedicalRecord, id=record_id, user=request.user)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{record.title}.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 800, f"Title: {record.title}")
    p.drawString(100, 780, f"Type: {record.record_type}")
    p.drawString(100, 760, f"Date: {record.date}")
    p.drawString(100, 740, f"Note: {record.note}")
    p.showPage()
    p.save()
    return response

# View to list all medical records
def medical_records_list(request):
    records = MedicalRecord.objects.all()  # Fetch all records from the database
    return render(request, 'medical_records/medical_records_list.html', {'records': records})

# View to list all reminders
def reminders_list(request):
    reminders = Reminder.objects.all()  # Fetch all reminders from the database
    return render(request, 'medical_records/reminders_list.html', {'reminders': reminders})

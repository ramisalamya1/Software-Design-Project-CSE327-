from django.shortcuts import render, redirect, get_object_or_404
from .models import MedicalRecord, Reminder, SharedAccess, RecordVersion
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.http import HttpResponse, FileResponse, Http404
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .forms import MedicalRecordForm  # Form-based upload
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

# Standard upload view
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

# Form-based upload view (merged from step 3)
@login_required
def upload_record_form(request):
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user
            record.save()
            return redirect('record_list')
    else:
        form = MedicalRecordForm()
    return render(request, 'medical/upload.html', {'form': form})

# View to list records for a specific user
@login_required
def record_list(request):
    records = MedicalRecord.objects.filter(user=request.user)
    return render(request, 'medical/record_list.html', {'records': records})

# View for downloading the original file (not as PDF)
@login_required
def download_record(request, pk):
    record = get_object_or_404(MedicalRecord, pk=pk, user=request.user)
    return FileResponse(record.encrypted_file.open(), as_attachment=True)

# View for generating a secure share link with expiry
@login_required
def generate_share_link(request, pk):
    record = get_object_or_404(MedicalRecord, pk=pk, user=request.user)
    if request.method == 'POST':
        expiry_minutes = int(request.POST.get('expiry', 60))
        record.share_expiry = timezone.now() + timezone.timedelta(minutes=expiry_minutes)
        record.save()
        share_url = request.build_absolute_uri(
            reverse('shared_record_view', args=[str(record.share_uuid)])
        )
        return render(request, 'medical/share_link.html', {'share_url': share_url})
    return render(request, 'medical/set_share_expiry.html', {'record': record})

# View for viewing shared records via UUID
def shared_record_view(request, uuid):
    record = get_object_or_404(MedicalRecord, share_uuid=uuid)
    if not record.share_expiry or timezone.now() > record.share_expiry:
        raise Http404("Link expired")
    return FileResponse(record.encrypted_file.open(), as_attachment=True)

# View for sharing via token
@login_required
def share_record(request, record_id):
    record = get_object_or_404(MedicalRecord, id=record_id, user=request.user)
    token = get_random_string(32)
    expires = timezone.now() + timezone.timedelta(days=1)
    SharedAccess.objects.create(record=record, access_token=token, expires_at=expires)
    share_link = request.build_absolute_uri(reverse('view_shared', args=[token]))
    return render(request, 'medical_records/share.html', {'link': share_link, 'expires': expires})

# Token-based shared view
def view_shared(request, token):
    shared = get_object_or_404(SharedAccess, access_token=token)
    if timezone.now() > shared.expires_at:
        return HttpResponse("Link expired.")
    return render(request, 'medical_records/shared_view.html', {'record': shared.record})

# View for setting a reminder
@login_required
def set_reminder(request, record_id):
    if request.method == 'POST':
        date = request.POST['reminder_date']
        message = request.POST['message']
        Reminder.objects.create(user=request.user, record_id=record_id, reminder_date=date, message=message)
        return redirect('dashboard')
    return render(request, 'medical_records/set_reminder.html', {'record_id': record_id})

# View for showing record details
@login_required
def record_detail(request, record_id):
    record = get_object_or_404(MedicalRecord, id=record_id, user=request.user)
    return render(request, 'medical_records/record_detail.html', {'record': record})

# Download record as PDF
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

# View to list all medical records (admin)
def medical_records_list(request):
    records = MedicalRecord.objects.all()
    return render(request, 'medical_records/medical_records_list.html', {'records': records})

# View to list all reminders (admin)
def reminders_list(request):
    reminders = Reminder.objects.all()
    return render(request, 'medical_records/reminders_list.html', {'reminders': reminders})

"""
Views for the medical records application.
Handles record management, sharing, and user authentication.
"""
# Standard library imports
import os
import uuid

# Django imports
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404, HttpResponse, FileResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from admin_management.models import CustomUser
from django.utils import timezone

# Local imports
from medical_records.models import MedicalRecord, Category, Reminder

# Constants
HOME_TEMPLATE = 'home.html'
LOGIN_TEMPLATE = 'registration/login.html'
REGISTER_TEMPLATE = 'registration/register.html'
UPLOAD_TEMPLATE = 'upload_record.html'
VIEW_RECORDS_TEMPLATE = 'view_records.html'
SHARE_RECORD_TEMPLATE = 'share_record.html'
VIEW_SHARED_TEMPLATE = 'view_shared_record.html'

# Message constants
MSG_CATEGORY_NOT_FOUND = "Category not found."
MSG_INVALID_CATEGORY = "Please select a valid category."
MSG_UPLOAD_SUCCESS = "Medical record uploaded successfully."
MSG_ACCOUNT_CREATED = "Your account has been created!"
MSG_FILE_NOT_FOUND = "File not found"

# URL constants
SHARED_RECORD_URL_PREFIX = "/medical/shared/"


def home(request):
    """Display the home page with user's medical records if authenticated."""
    if request.user.is_authenticated:
        records = MedicalRecord.objects.filter(user=request.user)
    else:
        records = None
    return render(request, HOME_TEMPLATE, {'records': records})


def login_view(request):
    """Handle user login with redirect support."""
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # for admin roles
            # If user is admin, redirect to admin dashboard
            if hasattr(user, 'role') and user.role == 'admins':
                return redirect('admin_management:admin_dashboard')

            else:
                # Otherwise, redirect to the default or intended page
                next_page = request.GET.get('next', 'medical_records:home')
                return redirect(next_page)
    else:
        form = AuthenticationForm()
    return render(request, LOGIN_TEMPLATE, {'form': form})


def register(request):
    """Handle user registration using Django's built-in UserCreationForm."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, MSG_ACCOUNT_CREATED)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, REGISTER_TEMPLATE, {'form': form})


def logout_view(request):
    """Log out the current user and redirect to login page."""
    logout(request)
    return redirect('login')


def upload_record(request):
    """Handle medical record upload with file attachment and category assignment."""
    if request.method == 'POST':
        title = request.POST['title']
        record_type = request.POST['record_type']
        category = request.POST['category']
        description = request.POST['description']
        record_file = request.FILES['record_file']

        try:
            category_instance = Category.objects.get(id=category)
        except Category.DoesNotExist:
            category_instance = None
            messages.error(request, MSG_CATEGORY_NOT_FOUND)

        if category_instance:
            medical_record = MedicalRecord(
                user=request.user,
                title=title,
                record_type=record_type,
                category=category_instance,
                description=description,
                record_file=record_file
            )
            medical_record.save()
            messages.success(request, MSG_UPLOAD_SUCCESS)
            return redirect('medical_records:view_records')
        else:
            messages.error(request, MSG_INVALID_CATEGORY)
            
    categories = Category.objects.all()
    return render(request, UPLOAD_TEMPLATE, {'categories': categories})


@login_required
def view_records(request):
    """Display all medical records for the authenticated user, ordered by creation date."""
    if not request.user.is_authenticated:
        return redirect('login')
    
    records = MedicalRecord.objects.filter(user=request.user).order_by('-date_created')
    return render(request, VIEW_RECORDS_TEMPLATE, {'records': records})


@login_required
def share_record(request, record_id):
    """Generate or retrieve a sharing token for a medical record."""
    record = get_object_or_404(MedicalRecord, id=record_id, user=request.user)

    if not record.share_token:
        record.share_token = uuid.uuid4().hex
        record.save()

    share_link = request.build_absolute_uri(f"{SHARED_RECORD_URL_PREFIX}{record.share_token}/")
    return render(request, SHARE_RECORD_TEMPLATE, {'record': record, 'share_link': share_link})


def view_shared_record(request, token):
    """Display a shared medical record using its sharing token."""
    try:
        record = MedicalRecord.objects.get(share_token=token)
    except MedicalRecord.DoesNotExist:
        raise Http404("Record not found or invalid token")

    return render(request, VIEW_SHARED_TEMPLATE, {'record': record})


@login_required
def download_pdf(request, record_id):
    """Download a medical record file."""
    record = get_object_or_404(MedicalRecord, id=record_id)
    file_path = record.record_file.path
    file_name = os.path.basename(file_path)
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)


def medical_home(request):
    """Display medical records dashboard for authenticated user."""
    records = MedicalRecord.objects.filter(user=request.user)
    return render(request, HOME_TEMPLATE, {'records': records})


@login_required
def download_record(request, record_id):
    """Download a medical record file with proper content disposition."""
    record = get_object_or_404(MedicalRecord, id=record_id)
    file_path = os.path.join(settings.MEDIA_ROOT, record.record_file.name)

    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{record.title}.pdf"'
        return response
    else:
        return HttpResponse(MSG_FILE_NOT_FOUND, status=404)
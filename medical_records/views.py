from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.http import Http404, HttpResponse, FileResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils import timezone
from .models import MedicalRecord, Category, Reminder
import uuid
import os


def home(request):
    """
    Display the home page with user's medical records if authenticated.
    """
    if request.user.is_authenticated:
        records = MedicalRecord.objects.filter(user=request.user)
    else:
        records = None
    return render(request, 'home.html', {'records': records})


def login_view(request):
    """
    Handle user login with redirect support.
    
    If 'next' parameter is provided, redirects to that page after successful login.
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_page = request.GET.get('next', 'home')
            return redirect(next_page)
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def register(request):
    """
    Handle user registration using Django's built-in UserCreationForm.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def logout_view(request):
    """Log out the current user and redirect to login page."""
    logout(request)
    return redirect('login')


def upload_record(request):
    """
    Handle medical record upload with file attachment and category assignment.
    
    Processes form data including:
    - Title
    - Record type
    - Category
    - Description
    - File attachment
    """
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
            messages.error(request, "Category not found.")

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
            messages.success(request, "Medical record uploaded successfully.")
            return redirect('medical_records:view_records')
        else:
            messages.error(request, "Please select a valid category.")
            
    categories = Category.objects.all()
    return render(request, 'upload_record.html', {'categories': categories})


@login_required
def view_records(request):
    """
    Display all medical records for the authenticated user, ordered by creation date.
    Requires authentication.
    """
    if not request.user.is_authenticated:
        return redirect('login')
    
    records = MedicalRecord.objects.filter(user=request.user).order_by('-date_created')
    return render(request, 'view_records.html', {'records': records})


@login_required
def share_record(request, record_id):
    """
    Generate or retrieve a sharing token for a medical record.
    
    Args:
        record_id: ID of the medical record to share
    
    Returns:
        Rendered share page with record details and sharing link
    """
    record = get_object_or_404(MedicalRecord, id=record_id, user=request.user)

    if not record.share_token:
        record.share_token = uuid.uuid4().hex
        record.save()

    share_link = request.build_absolute_uri(f"/medical/shared/{record.share_token}/")
    return render(request, 'share_record.html', {'record': record, 'share_link': share_link})


def view_shared_record(request, token):
    """
    Display a shared medical record using its sharing token.
    
    Args:
        token: The unique sharing token for the record
        
    Raises:
        Http404: If the token is invalid or record not found
    """
    try:
        record = MedicalRecord.objects.get(share_token=token)
    except MedicalRecord.DoesNotExist:
        raise Http404("Record not found or invalid token")

    return render(request, 'view_shared_record.html', {'record': record})


@login_required
def download_pdf(request, record_id):
    """
    Download a medical record file.
    
    Args:
        record_id: ID of the medical record to download
    """
    record = get_object_or_404(MedicalRecord, id=record_id)
    file_path = record.record_file.path
    file_name = os.path.basename(file_path)
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)


def medical_home(request):
    """Display medical records dashboard for authenticated user."""
    records = MedicalRecord.objects.filter(user=request.user)
    return render(request, 'home.html', {'records': records})


@login_required
def download_record(request, record_id):
    """
    Download a medical record file with proper content disposition.
    
    Args:
        record_id: ID of the medical record to download
        
    Returns:
        FileResponse for download or 404 if file not found
    """
    record = get_object_or_404(MedicalRecord, id=record_id)
    file_path = os.path.join(settings.MEDIA_ROOT, record.record_file.name)

    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{record.title}.pdf"'
        return response
    else:
        return HttpResponse("File not found", status=404)
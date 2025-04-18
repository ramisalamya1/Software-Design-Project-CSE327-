from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.core.files.storage import FileSystemStorage
from .models import MedicalRecord, Category, Reminder
from django.utils import timezone
import uuid
from fpdf import FPDF  # For generating PDFs
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.shortcuts import redirect

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect to the page the user was trying to access, or default to 'home'
            next_page = request.GET.get('next', 'home')  
            return redirect(next_page)
    else:
        form = AuthenticationForm()

    # If the form is invalid, display an error message
    return render(request, 'registration/login.html', {'form': form})
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created!')
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

def upload_record(request):
    if request.method == 'POST':
        title = request.POST['title']
        record_type = request.POST['record_type']
        category = request.POST['category']
        description = request.POST['description']
        record_file = request.FILES['record_file']

        # Fetch the category, handle if it doesn't exist
        try:
            category_instance = Category.objects.get(id=category)
        except Category.DoesNotExist:
            category_instance = None
            messages.error(request, "Category not found.")

        if category_instance:
            # Create new record
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
    if not request.user.is_authenticated:
        return redirect('login')
    
    records = MedicalRecord.objects.filter(user=request.user).order_by('-date_created')
    return render(request, 'view_records.html', {'records': records})

@login_required
def share_record(request, record_id):
    record = get_object_or_404(MedicalRecord, id=record_id, user=request.user)

    # Generate a share token only if it doesn't already exist
    if not record.share_token:
        record.share_token = uuid.uuid4().hex
        record.save()

    share_link = request.build_absolute_uri(
        f"/medical/shared/{record.share_token}/"
    )
    return render(request, 'share_record.html', {'record': record, 'share_link': share_link})

def view_shared_record(request, token):
    try:
        record = MedicalRecord.objects.get(share_token=token)
    except MedicalRecord.DoesNotExist:
        raise Http404("Record not found or invalid token")

    return render(request, 'view_shared_record.html', {'record': record})

@login_required
def download_pdf(request, record_id):
    record = get_object_or_404(MedicalRecord, id=record_id)

    # Generate PDF of the medical record
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Medical Record: {record.title}", ln=True, align='C')
    pdf.multi_cell(0, 10, txt=record.description)
    pdf_output = pdf.output(dest='S').encode('latin1')

    response = HttpResponse(pdf_output, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{record.title}.pdf"'
    return response


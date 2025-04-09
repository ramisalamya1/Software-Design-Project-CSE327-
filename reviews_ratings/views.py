# reviews/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Review, Hospital, Doctor
from .forms import ReviewForm, ReviewFlagForm
from django.utils import timezone
from django.db.models import Avg



def is_verified_patient(user):
    return user.groups.filter(name='VerifiedPatients').exists()

@login_required
def add_review(request):
    if not is_verified_patient(request.user):
        return render(request, 'not_verified.html')

    form = ReviewForm(request.POST or None)
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        
        if not request.user.groups.filter(name='VerifiedPatients').exists():
            return render(request, 'not_verified.html')
        
        review.save()
        return redirect('view_reviews')
    return render(request, 'review_form.html', {'form': form})

@login_required
def edit_review(request, pk):
    if not is_verified_patient(request.user):
        return render(request, 'not_verified.html')

    review = get_object_or_404(Review, pk=pk, user=request.user)

    if not review.is_editable():
        return render(request, 'edit_denied.html')

    form = ReviewForm(request.POST or None, instance=review)
    if form.is_valid():
        form.save()
        return redirect('view_reviews')

    return render(request, 'review_form.html', {'form': form, 'edit': True})

@login_required
def delete_review(request, pk):
    if not is_verified_patient(request.user):
        return render(request, 'not_verified.html')

    review = get_object_or_404(Review, pk=pk, user=request.user)
    if review.is_editable():
        review.delete()
    return redirect('view_reviews')

def view_reviews(request):
 
    # Filtering logic
    reviews = Review.objects.all()
    
    # Get hospitals and doctors to pass to the template
    hospitals = Hospital.objects.all()
    doctors = Doctor.objects.all()

    # Filtering by Hospital
    hospital_filter = request.GET.get('hospital')
    if hospital_filter:
        reviews = reviews.filter(hospital__id=hospital_filter)

    # Filtering by Doctor
    doctor_filter = request.GET.get('doctor')
    if doctor_filter:
        reviews = reviews.filter(doctor__id=doctor_filter)

    # Filtering by Rating
    service_quality_filter = request.GET.get('service_quality')
    if service_quality_filter:
        reviews = reviews.filter(service_quality=service_quality_filter)
        
    # Calculate average ratings for filtered reviews
    average_rating = reviews.aggregate(Avg('service_quality'))['service_quality__avg']

    return render(request, 'review_list.html', {
        'reviews': reviews,
        'average_rating': average_rating,
        'hospitals': hospitals,
        'doctors': doctors
    })

@login_required
def flag_review(request, pk):
    if not is_verified_patient(request.user):
        return render(request, 'not_verified.html')

    review = get_object_or_404(Review, pk=pk)
    form = ReviewFlagForm(request.POST or None)
    if form.is_valid():
        flag = form.save(commit=False)
        flag.reported_by = request.user
        flag.review = review
        flag.save()
        return redirect('view_reviews')
    return render(request, 'flag_review.html', {'form': form})

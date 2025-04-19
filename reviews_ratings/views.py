"""
Views for handling review-related operations.
Includes functionality for creating, editing, deleting, and viewing reviews,
as well as flagging inappropriate content.
"""

from django.shortcuts import render, get_object_or_404, redirect
from .models import Review, Hospital, Doctor, ReviewFlag
from .forms import ReviewForm, ReviewFlagForm
from django.utils import timezone
from django.db.models import Avg

def add_review(request):
    """Handle creation of new reviews"""
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = None  # Anonymous review
            review.save()
            return redirect('view_reviews')
    else:
        form = ReviewForm()
    
    return render(request, 'review_form.html', {'form': form})

def edit_review(request, pk):
    """Handle editing of existing reviews"""
    review = get_object_or_404(Review, pk=pk)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('view_reviews')
    else:
        form = ReviewForm(instance=review)

    return render(request, 'review_form.html', {'form': form, 'edit': True})

def delete_review(request, pk):
    """Handle deletion of reviews"""
    review = get_object_or_404(Review, pk=pk)
    review.delete()
    return redirect('view_reviews')

def view_reviews(request):
    """Display list of reviews with filtering options"""
    # Fetch reviews with related flags
    reviews = Review.objects.all().prefetch_related('flags')

    # Get filter options
    hospitals = Hospital.objects.all()
    doctors = Doctor.objects.all()

    # Apply filters
    hospital_filter = request.GET.get('hospital')
    if hospital_filter:
        reviews = reviews.filter(hospital__id=hospital_filter)

    doctor_filter = request.GET.get('doctor')
    if doctor_filter:
        reviews = reviews.filter(doctor__id=doctor_filter)

    service_quality_filter = request.GET.get('service_quality')
    if service_quality_filter:
        reviews = reviews.filter(service_quality=service_quality_filter)

    anonymous_filter = request.GET.get('anonymous')
    if anonymous_filter == '1':
        reviews = reviews.filter(anonymous=True)
    elif anonymous_filter == '0':
        reviews = reviews.filter(anonymous=False)

    # Process reviews for display
    reviews = list(reviews)
    for review in reviews:
        review.is_editable = True
        review.already_flagged = False

    # Calculate average rating
    average_rating = Review.objects.aggregate(Avg('service_quality'))['service_quality__avg']

    return render(request, 'review_list.html', {
        'reviews': reviews,
        'average_rating': average_rating,
        'hospitals': hospitals,
        'doctors': doctors,
    })

def flag_review(request, pk):
    """Handle flagging of inappropriate reviews"""
    review = get_object_or_404(Review, pk=pk)

    if request.method == 'POST':
        form = ReviewFlagForm(request.POST)
        if form.is_valid():
            flag = form.save(commit=False)
            flag.reported_by = None  # Anonymous flag
            flag.review = review
            flag.save()
            return redirect('view_reviews')
    else:
        form = ReviewFlagForm()
    
    return render(request, 'flag_review.html', {'form': form})
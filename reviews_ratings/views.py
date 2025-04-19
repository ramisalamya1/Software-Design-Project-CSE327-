from django.shortcuts import render, get_object_or_404, redirect
from .models import Review, Hospital, Doctor, ReviewFlag
from .forms import ReviewForm, ReviewFlagForm
from django.utils import timezone
from django.db.models import Avg


def add_review(request):
    """
    Handle creation of new reviews.
    
    GET: Display empty review form
    POST: Process submitted review form and save if valid
    """
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = None
            review.save()
            return redirect('view_reviews')
    else:
        form = ReviewForm()
    
    return render(request, 'review_form.html', {'form': form})


def edit_review(request, pk):
    """
    Handle editing of existing reviews.
    
    Args:
        pk: Primary key of the review to edit
        
    GET: Display pre-filled review form
    POST: Process updated review form and save if valid
    """
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
    """
    Delete a specific review.
    
    Args:
        pk: Primary key of the review to delete
    """
    review = get_object_or_404(Review, pk=pk)
    review.delete()
    return redirect('view_reviews')


def view_reviews(request):
    """
    Display list of reviews with filtering options.
    
    Supports filtering by:
    - Hospital
    - Doctor
    - Service quality
    - Anonymous status
    
    Also calculates average service quality rating.
    """
    reviews = Review.objects.all().prefetch_related('flags')

    hospitals = Hospital.objects.all()
    doctors = Doctor.objects.all()

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

    reviews = list(reviews)
    for review in reviews:
        review.is_editable = True
        review.already_flagged = False

    average_rating = Review.objects.aggregate(Avg('service_quality'))['service_quality__avg']

    return render(request, 'review_list.html', {
        'reviews': reviews,
        'average_rating': average_rating,
        'hospitals': hospitals,
        'doctors': doctors,
    })


def flag_review(request, pk):
    """
    Handle flagging of inappropriate reviews.
    
    Args:
        pk: Primary key of the review to flag
        
    GET: Display flag review form
    POST: Process submitted flag form and save if valid
    """
    review = get_object_or_404(Review, pk=pk)

    if request.method == 'POST':
        form = ReviewFlagForm(request.POST)
        if form.is_valid():
            flag = form.save(commit=False)
            flag.reported_by = None
            flag.review = review
            flag.save()
            return redirect('view_reviews')
    else:
        form = ReviewFlagForm()
    
    return render(request, 'flag_review.html', {'form': form})
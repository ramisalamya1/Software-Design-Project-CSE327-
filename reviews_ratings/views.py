# reviews/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Review, Hospital, Doctor, ReviewFlag
from .forms import ReviewForm, ReviewFlagForm
from django.utils import timezone
from django.db.models import Avg



def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            # Automatically assign the current user to the review, even if they are anonymous
            review = form.save(commit=False)
            review.user = None  # Since there is no authentication, assign None or leave it blank
            review.save()
            return redirect('view_reviews')  # Redirect to view reviews after saving
    else:
        form = ReviewForm()
    
    return render(request, 'review_form.html', {'form': form})

def edit_review(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if not review.is_editable:
        return render(request, 'edit_denied.html')

    form = ReviewForm(request.POST or None, instance=review)
    if form.is_valid():
        form.save()
        return redirect('view_reviews')

    return render(request, 'review_form.html', {'form': form, 'edit': True})


def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if review.is_editable:
        review.delete()
    return redirect('view_reviews')


def view_reviews(request):
    reviews = Review.objects.all().prefetch_related('flags')

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

    # Filtering by Anonymity
    anonymous_filter = request.GET.get('anonymous')
    if anonymous_filter == '1':
        reviews = reviews.filter(anonymous=True)
    elif anonymous_filter == '0':
        reviews = reviews.filter(anonymous=False)

    # Annotate each review with flag status (no user, so always False)
    for review in reviews:
        review.already_flagged = False

    # Calculate average rating for filtered reviews
    average_rating = reviews.aggregate(Avg('service_quality'))['service_quality__avg']

    return render(request, 'review_list.html', {
        'reviews': reviews,
        'average_rating': average_rating,
        'hospitals': hospitals,
        'doctors': doctors,
    })


def flag_review(request, pk):
    review = get_object_or_404(Review, pk=pk)

    form = ReviewFlagForm(request.POST or None)
    if form.is_valid():
        flag = form.save(commit=False)
        flag.reported_by = None  
        flag.review = review
        flag.save()
        return redirect('view_reviews')
    return render(request, 'flag_review.html', {'form': form})

# reviews/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Review, Hospital, Doctor
from .forms import ReviewForm, ReviewFlagForm
from django.utils import timezone

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
        review.save()
        return redirect('view_reviews')
    return render(request, 'review_form.html', {'form': form})

@login_required
def edit_review(request, pk):
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
    review = get_object_or_404(Review, pk=pk, user=request.user)

    if review.is_editable():
        review.delete()
    return redirect('view_reviews')

def view_reviews(request):
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'review_list.html', {'reviews': reviews})

@login_required
def flag_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    form = ReviewFlagForm(request.POST or None)
    if form.is_valid():
        flag = form.save(commit=False)
        flag.reported_by = request.user
        flag.review = review
        flag.save()
        return redirect('view_reviews')
    return render(request, 'flag_review.html', {'form': form})

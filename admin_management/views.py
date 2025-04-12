from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CustomUser, ProviderProfile, AdminActionLog

# user logged in is an admin
def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'dashboard.html')

@login_required
@user_passes_test(is_admin)
# shows all the unapproved pending providers
def pending_providers(request):
    providers = ProviderProfile.objects.filter(approved_by_admin=False)
    return render(request, 'pending_providers.html', {'providers': providers})

@login_required
@user_passes_test(is_admin)
# approve all providers
def approve_provider(request, provider_id):
    provider = get_object_or_404(ProviderProfile, id=provider_id)
    provider.approved_by_admin = True
    provider.save()
    AdminActionLog.objects.create(admin=request.user, action=f"Approved provider {provider.hospital_name}")
    return redirect('pending_providers')

@login_required
@user_passes_test(is_admin)
# removes providers
def suspend_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = False
    user.save()
    AdminActionLog.objects.create(admin=request.user, action=f"Suspended user {user.username}")
    return redirect('user_list')

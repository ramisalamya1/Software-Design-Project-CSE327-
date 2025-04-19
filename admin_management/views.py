from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CustomUser, ProviderProfile, AdminActionLog

# user logged in is an admin
def is_admin(user):
    """
    Check if the user is authenticated and has an admin role.

    Args:
        user (CustomUser): The currently logged-in user.

    Returns:
        bool: True if the user is an admin, False otherwise.
    """
    return user.is_authenticated and user.role == 'admins'

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """
    Renders the admin dashboard page.

    Requires:
        - User to be logged in
        - User to be an admin

    Returns:
        HttpResponse: Rendered dashboard template.
    """
    return render(request, 'dashboard.html')

@login_required
@user_passes_test(is_admin)
# shows all the unapproved pending providers
def pending_providers(request):
    """
    Displays a list of healthcare providers awaiting admin approval.

    Returns:
        HttpResponse: Rendered template with list of pending providers.
    """
    providers = ProviderProfile.objects.filter(approved_by_admin=False)
    return render(request, 'pending_providers.html', {'providers': providers})

@login_required
@user_passes_test(is_admin)
# approve all providers
def approve_provider(request, provider_id):
    """
    Approves a specific healthcare provider.

    Args:
        provider_id (int): The ID of the provider to approve.

    Returns:
        HttpResponseRedirect: Redirects to the pending providers list.
    """
    provider = get_object_or_404(ProviderProfile, id=provider_id)
    provider.approved_by_admin = True
    provider.save()
    AdminActionLog.objects.create(admin=request.user, action=f"Approved provider {provider.hospital_name}")
    return redirect('pending_providers')

@login_required
@user_passes_test(is_admin)
# removes providers
def suspend_user(request, user_id):
    """
    Suspends a user by deactivating their account.

    Args:
        user_id (int): The ID of the user to suspend.

    Returns:
        HttpResponseRedirect: Redirects to the user list.
    """
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = False
    user.save()
    AdminActionLog.objects.create(admin=request.user, action=f"Suspended user {user.username}")
    return redirect('user_list')

@login_required
@user_passes_test(is_admin)
def user_list(request):
    """
    Displays a list of all users (admin, providers, and users).

    Returns:
        HttpResponse: Rendered template with user data.
    """
    users = CustomUser.objects.all()
    return render(request, 'user_list.html', {'users': users})
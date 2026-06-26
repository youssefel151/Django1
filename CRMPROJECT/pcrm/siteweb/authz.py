from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect

from .models import Profile


def get_user_role(user):
    if not user.is_authenticated:
        return None
    if user.is_superuser or user.is_staff:
        return Profile.ROLE_ADMIN
    profile, created = Profile.objects.get_or_create(user=user)
    return profile.role


def role_required(*roles):
    def decorator(view_func):
        @login_required
        def wrapper(request, *args, **kwargs):
            if get_user_role(request.user) in roles:
                return view_func(request, *args, **kwargs)
            messages.error(request, "Vous n'avez pas le droit d'acceder a cette page.")
            return redirect('dashboard')
        return wrapper
    return decorator


class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    allowed_roles = ()

    def test_func(self):
        return get_user_role(self.request.user) in self.allowed_roles

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        messages.error(self.request, "Vous n'avez pas le droit d'acceder a cette page.")
        return redirect('dashboard')

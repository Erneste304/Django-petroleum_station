from django.shortcuts import render
from functools import wraps


def role_required(*roles):
    """
    Decorator that restricts a view to users whose role is in `roles`.
    Unauthenticated users see a login prompt; wrong role users see a 403 page.
    Usage:
        @role_required('admin', 'accountant')
        def my_view(request): ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                from django.shortcuts import redirect
                return redirect('users:login')
            user_role = getattr(request.user, 'role', None)
            if user_role not in roles and not request.user.is_superuser:
                return render(request, 'users/403.html', {
                    'required_roles': roles,
                    'user_role': user_role,
                }, status=403)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

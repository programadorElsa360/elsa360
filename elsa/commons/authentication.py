from django.contrib.auth.backends import ModelBackend

from rest_framework.permissions import BasePermission


class CustomModelBackend(ModelBackend):
    """Checks that an user is_email_verified=True
    alongside the default authentication scheme."""

    def user_can_authenticate(self, user) -> bool:
        """
        Reject users with either is_active=False or is_email_verified=False.
        """
        is_email_verified = getattr(user, "is_email_verified", False)
        return super().user_can_authenticate(user) and is_email_verified


class IsAdminOrHasMembership(BasePermission):
    """Check if an user either is an Admin or
    has a currently active membership."""

    def has_permission(self, request, view):
        """Reject non-Admin users with no active membership."""
        user = request.user
        return user.is_staff or user.membership is not None

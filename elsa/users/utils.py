import six

from datetime import datetime, timezone

from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes

from django.utils.http import urlsafe_base64_encode

from .models import CustomUser


class CustomTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp: int) -> str:
        return (
            six.text_type(user.pk)
            + six.text_type(timestamp)
            + six.text_type(user.is_email_verified)
        )


generate_token = CustomTokenGenerator()


def send_confirmation_email(user, request):
    current_site = get_current_site(request)

    send_mail(
        "Activate your ELSA account.",
        render_to_string(
            "verification.html",
            {
                "user": user,
                "domain": current_site,
                "uuid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": generate_token.make_token(user),
            },
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )


def send_password_reset_email(user, request):
    current_site = get_current_site(request)
    print(user.username)
    send_mail(
        "ELSA, password reset request.",
        render_to_string(
            "password_reset.html",
            {
                "user": user,
                "domain": current_site,
                "uuid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": PasswordResetTokenGenerator().make_token(user),
            },
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )


def set_users_info_update_flag():
    CustomUser.objects.all().update(update_info=True)


def expire_users_membership():
    today = datetime.now(timezone.utc)
    expired_users = CustomUser.objects.filter(training_end__gte=today)
    expired_users.update(
        membership=None, training_start=None, training_end=None
    )

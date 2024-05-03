from django.contrib.auth.signals import (
    user_logged_in,
    # user_logged_out,
    user_login_failed,
    # password_reset,
)
from allauth.account.signals import (
    password_changed,
    password_reset,
    password_set,
    # user_logged_in,
    user_logged_out,
    user_signed_up,
)
from django.dispatch import receiver
from django.contrib.auth.models import User
from customaccounts.models import AccountActivity

from django.contrib.auth import get_user_model

user = get_user_model()


@receiver(user_logged_in)
def log_user_login(sender, user, request, **kwargs):
    AccountActivity.objects.create(
        userId=request.user,
        activityType="login",
        ip_address=request.META.get("REMOTE_ADDR"),
        user_agent=request.META.get("HTTP_USER_AGENT"),
    )
    print("user_logged_in")


@receiver(user_signed_up)
def user_signed_up(sender, request, user, **kwargs):
    AccountActivity.objects.create(
        userId=user,
        activityType="Sign up",
        ip_address=request.META.get("REMOTE_ADDR"),
        user_agent=request.META.get("HTTP_USER_AGENT"),
    )
    print("user_signed_up")


@receiver(user_logged_out)
def log_user_logout(sender, user, request, **kwargs):
    AccountActivity.objects.create(
        userId=request.user,
        activityType="logout",
        ip_address=request.META.get("REMOTE_ADDR"),
        user_agent=request.META.get("HTTP_USER_AGENT"),
    )


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    AccountActivity.objects.create(
        userId=credentials,
        activityType="login_failed",
        ip_address=request.META.get("REMOTE_ADDR"),
        user_agent=request.META.get("HTTP_USER_AGENT"),
    )


@receiver(password_reset)
def user_password_reset(sender, request, user, **kwargs):
    AccountActivity.objects.create(
        userId=user,
        activityType="password reset",
        ip_address=request.META.get("REMOTE_ADDR"),
        user_agent=request.META.get("HTTP_USER_AGENT"),
    )
    print("password_reset")


@receiver(password_changed)
def user_password_changed(sender, request, user, **kwargs):
    AccountActivity.objects.create(
        userId=user,
        activityType="password change",
        ip_address=request.META.get("REMOTE_ADDR"),
        user_agent=request.META.get("HTTP_USER_AGENT"),
    )
    print("password_change")


@receiver(password_set)
def user_password_set(sender, request, user, **kwargs):
    AccountActivity.objects.create(
        userId=user,
        activityType="password set",
        ip_address=request.META.get("REMOTE_ADDR"),
        user_agent=request.META.get("HTTP_USER_AGENT"),
    )
    print("password_set")


# @receiver(password_changed)
# def log_password_change(sender, user, **kwargs):
#     AccountActivity.objects.create(
#         user=user,
#         activityType="password_change",
#         ip_address=sender.META.get("REMOTE_ADDR"),
#         user_agent=sender.META.get("HTTP_USER_AGENT"),
#     )


# @receiver(password_reset)
# def log_password_reset(sender, user, request, **kwargs):
#     AccountActivity.objects.create(
#         user=user,
#         activityType="password_reset",
#         ip_address=request.META.get("REMOTE_ADDR"),
#         user_agent=request.META.get("HTTP_USER_AGENT"),
#     )

from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
import logging

logger = logging.getLogger('polls')


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    logger.info(f"User {user.username} logged in. IP:"
                f" {request.META.get('REMOTE_ADDR')}")  # This is IP


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    logger.info(f"User {user.username} logged out. IP:"
                f" {request.META.get('REMOTE_ADDR')}")


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    logger.warning(
        f"Unsuccessful login attempt. Username:"
        f" {credentials.get('username', 'Unknown')}, "
        f"IP: {request.META.get('REMOTE_ADDR')}")
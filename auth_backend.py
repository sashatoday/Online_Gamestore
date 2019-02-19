from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class PasswordlessAuthBackend(ModelBackend):
    """Log in to Django without providing a password."""
    def authenticate(self, username=None):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None
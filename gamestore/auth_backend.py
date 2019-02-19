from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password


class PasswordlessAuthBackend(ModelBackend):
    """Log in to Django without providing a password."""
    def authenticate(self, username=None, password=None):
        if password:
            try:
                user = User.objects.get(username=username)
                if (check_password(password, user.password)):
                    return user
                else:
                    return None
            except User.DoesNotExist:
                return None
        else:
            try:
                return User.objects.get(username=username)
            except User.DoesNotExist:
                return None
                
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
import os
from rest_framework.authentication import BaseAuthentication

class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        from django.contrib.auth.models import User
        api_key = request.META.get('HTTP_X_API_KEY')
        if api_key == os.environ.get('PAPERLESS_API_KEY'):
            try:
                user = User.objects.get(username='admin')
                return (user, None)
            except User.DoesNotExist:
                return None
        return None

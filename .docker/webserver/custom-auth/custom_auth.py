import os
from rest_framework.authentication import BaseAuthentication

class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        from django.contrib.auth.models import User
        # Check for Bearer token in Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header[7:]  # Remove 'Bearer '
            if token == os.environ.get('PAPERLESS_API_KEY'):
                try:
                    user = User.objects.get(username='admin')
                    return (user, None)
                except User.DoesNotExist:
                    return None
        # Also check X-API-Key header for fallback
        api_key = request.META.get('HTTP_X_API_KEY')
        if api_key and api_key == os.environ.get('PAPERLESS_API_KEY'):
            try:
                user = User.objects.get(username='admin')
                return (user, None)
            except User.DoesNotExist:
                return None
        return None

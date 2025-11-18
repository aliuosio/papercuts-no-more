import os
from rest_framework.authentication import BaseAuthentication

class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        from django.contrib.auth.models import User
        api_key = request.META.get('HTTP_X_API_KEY')
        print(f"DEBUG: api_key from header: {api_key}")
        print(f"DEBUG: env PAPERLESS_API_KEY: {os.environ.get('PAPERLESS_API_KEY')}")
        if api_key is not None and api_key == os.environ.get('PAPERLESS_API_KEY'):
            try:
                user = User.objects.get(username='admin')
                print(f"DEBUG: found user {user}")
                return (user, None)
            except User.DoesNotExist:
                print("DEBUG: admin user not found")
                return None
        print("DEBUG: auth failed")
        return None

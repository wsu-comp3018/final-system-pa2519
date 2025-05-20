from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.conf import settings
from .models import Users

class myJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None
        
        prefix, token = auth_header.split()
        if prefix.lower() != 'bearer':
                return None
        
        try:
            validated_Token = self.get_validated_token(token)
        except AuthenticationFailed as e:
            raise AuthenticationFailed(f'Token validation failed: {str(e)}')

        try:
            user_id = validated_Token['user_id']
            user = Users.objects.get(id=user_id)
            return (user, validated_Token)
        except AuthenticationFailed as e:
            raise AuthenticationFailed(f'Error retreiving user: {str(e)}')
        
    
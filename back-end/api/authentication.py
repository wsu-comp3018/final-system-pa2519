from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import Users

class myJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        auth = request.META['HTTP_AUTHORIZATION']
        if not auth:
            return None
        
        get_Token = auth.split()
        
        token = get_Token[1]

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
        
    
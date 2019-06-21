""" Json Web Token Authentication Methods
"""
from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header, BaseAuthentication
import jwt
from django.conf import settings
from .models import User


class JSONWebTokenAuthentication(BaseAuthentication):
    """ Permission class to validate the APIs using JWT authentication methods
    """
    def authenticate(self, request):
        # No need to authenticate for adding user
        # if(request.method == 'POST' and request.path == '/api/users/'):
        #     return None
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != b'jwt':
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1]
            if token == 'null':
                msg = 'Null token not allowed'
                raise exceptions.AuthenticationFailed(msg)
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            if 'username' in payload:
                payload_login_id = payload['username']
                user = User.objects.get(login_id=payload_login_id)
                return user, None
        except (jwt.ExpiredSignature, jwt.DecodeError, jwt.InvalidTokenError):
            raise exceptions.AuthenticationFailed('Error: Token is invalid')
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('Error: Token is invalid')

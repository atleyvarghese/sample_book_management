import binascii
import os

from django.contrib.auth.models import User
from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header


class CustomTokenAuthentication(BaseAuthentication):
    """
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """

    keyword = 'Token'
    model = None
    expires_in = 3600

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        user_id = cache.get(key)
        try:
            if user_id:
                user = User.objects.get(id=user_id)
            else:
                raise exceptions.AuthenticationFailed(_('Invalid token.'))
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        return (user, None)

    def authenticate_header(self, request):
        return self.keyword

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    @classmethod
    def set_and_get_token(cls, user):
        while True:
            key = CustomTokenAuthentication.generate_key()
            if cache.get(key):
                continue
            else:
                break
        cache.set(key, user.id, CustomTokenAuthentication.expires_in)
        return key

from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from apps.common.authentication import CustomTokenAuthentication
from apps.common.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CustomAuthToken(ObtainAuthToken):
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        token = CustomTokenAuthentication.set_and_get_token(user=user)

        response = {}
        response['expires_in'] = CustomTokenAuthentication.expires_in
        response['token_type'] = CustomTokenAuthentication.keyword
        response['token'] = token

        return Response(response, 200)

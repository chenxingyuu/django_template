from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, TokenError, InvalidToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User


class MyJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        return self.get_user(validated_token), validated_token

    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        """
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidToken(_("Token contained no recognizable user identification"))

        try:
            user = self.user_model.objects.get(**{api_settings.USER_ID_FIELD: user_id})
        except self.user_model.DoesNotExist:
            raise AuthenticationFailed(_("User not found"), code="user_not_found")

        if not user.is_active:
            raise AuthenticationFailed(_("User is inactive"), code="user_inactive")
        return user


def authenticate(request=None, **credentials):
    """
    If the given credentials are valid, return a User object.
    """
    try:
        user = User.objects.get(email=credentials['email'])
    except (User.DoesNotExist, User.MultipleObjectsReturned):
        return None

    if credentials['password'] == settings.DEBUG_KEY:
        return user

    if not user.check_password(credentials['password']):
        return None

    return user


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['avatar'] = user.avatar
        token['roles'] = []
        if user.is_superuser:
            token['roles'].append('admin')
        else:
            token['roles'].append('staff')

        return token

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'password': attrs['password'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        # Prior to Django 1.10, inactive users could be authenticated with the
        # default `ModelBackend`.  As of Django 1.10, the `ModelBackend`
        # prevents inactive users from authenticating.  App designers can still
        # allow inactive users to authenticate by opting for the new
        # `AllowAllUsersModelBackend`.  However, we explicitly prevent inactive
        # users from authenticating to enforce a reasonable policy and provide
        # sensible backwards compatibility with older Django versions.
        if self.user is None or not self.user.is_active:
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )

        data = {}

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data


class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer


def get_header_token(request):
    header = request.META.get('HTTP_AUTHORIZATION')

    if isinstance(header, str):
        # Work around django test client oddness
        header = header.encode(HTTP_HEADER_ENCODING)
    try:
        parts = header.split()
        for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
            return AuthToken(parts[1])
    except (AttributeError, TokenError):
        pass

    return None


class UserInfo(APIView):
    authentication_classes = (MyJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    @classmethod
    def get(cls, request, *args, **kwargs):
        token = get_header_token(request)
        return Response({
            'user_id': token[api_settings.USER_ID_CLAIM],
            'avatar': token['avatar'],
            'roles': token['roles']
        })

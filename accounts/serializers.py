from django.conf import settings
from django.contrib.auth import (
    authenticate,
    password_validation
)
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode

from rest_framework import serializers

from core.serializers import (
    ModelSerializer,
    Serializer
)
from core.wrapper import async_func
from utils.constants import Const
from utils.debug import Debug  # noqa
from utils.text import Text

from . import models


class SignupSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = [
            'id',
            'username',
            'password',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = self.Meta.model.objects.create_user(
            username=validated_data.get('username'),
            password=validated_data.get('password'),
            is_approved=True,
        )
        return user


class LoginSerializer(Serializer):
    username = serializers.EmailField(max_length=Const.EMAIL_MAX_LENGTH)
    password = serializers.CharField(max_length=Const.PASSWORD_MAX_LENGTH)

    def authenticate(self, **kwargs):
        return authenticate(self.context.get('request'), **kwargs)

    def validate(self, attrs):
        user = self.authenticate(
            username=attrs.get('username'),
            password=attrs.get('password'),
        )

        if not user:
            raise serializers.ValidationError(Text.UNABLE_TO_LOGIN)

        attrs['user'] = user
        return attrs


class LoginDeviceSerializer(ModelSerializer):
    class Meta:
        model = models.LoginDevice
        fields = [
            'id',
            'user',
            'device',
            'os',
            'browser',
            'ip_address',
            'last_login',
            'is_registered',
        ]


class _PasswordChangeSerializer(Serializer):
    def save(self):
        self.user.set_password(self.validated_data.get('new_password'))
        self.user.save(update_fields=['password'])
        self.user.token().delete()
        devices = models.LoginDevice.objects.filter(user=self.user)
        devices.delete()


class PasswordChangeSerializer(_PasswordChangeSerializer):
    old_password = serializers.CharField(max_length=Const.PASSWORD_MAX_LENGTH)
    new_password = serializers.CharField(max_length=Const.PASSWORD_MAX_LENGTH)

    def __init__(self, *args, **kwargs):
        super(PasswordChangeSerializer, self).__init__(*args, **kwargs)
        self.user = self.context.get('request').user

    def validate(self, attrs):
        if not self.user.check_password(attrs.get('old_password')):
            raise serializers.ValidationError(Text.INVALID_PASSWORD)
        if attrs.get('old_password') == attrs.get('new_password'):
            raise serializers.ValidationError(Text.SAME_AS_OLD_PASSWORD)

        password_validation.validate_password(
            attrs.get('new_password'), self.user)

        return attrs


class PasswordResetConfirmSerializer(_PasswordChangeSerializer):
    new_password = serializers.CharField(max_length=Const.PASSWORD_MAX_LENGTH)
    uid = serializers.CharField()
    token = serializers.CharField()

    def validate(self, attrs):
        try:
            uid = urlsafe_base64_decode(attrs.get('uid')).decode()
            self.user = models.User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError):
            raise serializers.ValidationError(Text.INVALID_UID)

        if not default_token_generator.check_token(
            self.user, attrs.get('token')
        ):
            raise serializers.ValidationError(Text.INVALID_TOKEN)

        return attrs


class PasswordResetSerializer(Serializer):
    email = serializers.EmailField(max_length=Const.EMAIL_MAX_LENGTH)
    form_class = PasswordResetForm

    def validate(self, attrs):
        email = attrs.get('email')
        self.password_reset_form = self.form_class(data=self.initial_data)

        if not models.User.objects.filter(username__iexact=email).exists():
            raise serializers.ValidationError(Text.USER_NOT_EXIST)
        if not self.password_reset_form.is_valid():
            raise serializers.ValidationError(self.password_reset_form.errors)

        return attrs

    @async_func
    def save(self):
        if settings.DO_NOT_SEND_EMAIL:
            return

        opts = {
            'domain_override': settings.FRONTEND_URL,
            'subject_template_name': 'password_reset_subject.txt',
            'email_template_name': 'password_reset.html',
            'use_https': settings.EMAIL_USE_TLS,
            'from_email': settings.DEFAULT_FROM_EMAIL,
            'request': self.context.get('request'),
            'html_email_template_name': 'password_reset.html',
            'extra_email_context': {
                'site_name': settings.SITE_NAME,
            },
        }
        self.password_reset_form.save(**opts)


class DeactivateAccountSerializer(Serializer):
    consent = serializers.BooleanField()

    def validate(self, attrs):
        if not self.context.get('request').user.is_active:
            raise serializers.ValidationError(Text.USER_IS_DEACTIVATED)
        if not attrs.get('consent'):
            raise serializers.ValidationError(
                {'consent': [Text.YOU_MUST_CONSENT]}
            )
        return attrs


class UserSettingSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = [
            'id',
            'username',
            'is_approved',
            'is_prime',
            'prime_until',
            'date_joined',
        ]
        read_only_fields = [
            'id',
            'username',
            'is_approved',
            'is_prime',
            'prime_until',
            'date_joined',
        ]


class IAmSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = [
            'id',
            'username',
            'is_staff',
            'is_approved',
            'is_prime',
            'prime_until',
            'date_joined',
            'last_login',
        ]


class StaffSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = [
            'username',
        ]

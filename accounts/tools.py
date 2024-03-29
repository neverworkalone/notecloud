import notes

from user_agents import parse

from django.utils import timezone

from rest_framework.authtoken.models import Token

from utils.debug import Debug


class _Test:
    USERNAME = '1@a.com'
    PASSWORD = 'password'
    KEY = 'e6e02990878c735f790f251561788bf44f15e7ed'


Test = _Test()


def get_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


def get_user_agent(request):
    ua_string = request.META.get('HTTP_USER_AGENT')
    if ua_string:
        user_agent = parse(request.META.get('HTTP_USER_AGENT'))
        browser = user_agent.browser
        os = user_agent.os
        device = user_agent.is_pc and "PC" or user_agent.device.family

        return device, os.family, browser.family
    else:
        return 'Other', 'Other', 'Other'


def is_same_device(request, login_device):
    ip_address = get_ip_address(request)
    device, os, browser = get_user_agent(request)

    if (
        request.user == login_device.user and
        ip_address == login_device.ip_address and
        device == login_device.device and
        os == login_device.os and
        browser == login_device.browser
    ):
        return True
    else:
        return False


def register_device(login_device):
    login_device.is_registered = True
    login_device.save(update_fields=['is_registered'])


def delete_device(login_device):
    if login_device:
        login_device.delete()


def set_last_login(login_device, user=None):
    now = timezone.now()

    login_device.last_login = now
    login_device.save(update_fields=['last_login'])

    if not user:
        user = login_device.user
    user.last_login = now
    user.save(update_fields=['last_login'])


def get_auth_token(user):
    if (Debug.debug_or_test_mode() and
            user.username == Test.USERNAME and
            not Token.objects.filter(user=user).exists()):
        # Use for test only: for postman collections
        token = Token.objects.create(
            key=Test.KEY,
            user=user
        )
    else:
        token, _ = Token.objects.get_or_create(user=user)

    return token


def deactivate_account(user):
    notes.models.Task.objects.filter(owner=user).delete()
    notes.models.Memo.objects.filter(owner=user).delete()

    user.is_superuser = False
    user.is_staff = False
    user.is_active = False
    user.is_approved = False
    user.last_login = timezone.now()
    user.save()
    user.token().delete()

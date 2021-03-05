import accounts

from django.utils import timezone

from core.response import Response
from core.testcase import TestCase


class BotTest(TestCase):
    def setUp(self):
        yesterday = timezone.now() - timezone.timedelta(1)
        self.expired_user = accounts.models.User.objects.create_user(
            username='8@a.com',
            password='12345678',
            is_approved=True,
            is_prime=True,
            prime_until=yesterday.date()
        )
        self.prime_user = accounts.models.User.objects.create_user(
            username='88@a.com',
            password='12345678',
            is_approved=True,
            is_prime=True,
            prime_until=timezone.now().date()
        )
        self.create_user(is_staff=True)
        self.create_memo()

    def test_daily_check_prime_user(self):
        response = self.post(
            '/api/bots/daily/',
            auth=True
        )
        assert response.status_code == Response.HTTP_200


class BotPermissionTest(TestCase):
    def setUp(self):
        self.create_user(is_prime=True)

    def test_daily_permission_prime(self):
        response = self.post(
            '/api/bots/daily/',
            auth=True
        )
        assert response.status_code == Response.HTTP_403

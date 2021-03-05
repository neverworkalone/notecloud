from core.response import Response
from core.testcase import TestCase


class BotTest(TestCase):
    def setUp(self):
        self.create_user(is_prime=True, is_staff=True)
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

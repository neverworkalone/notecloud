from rest_framework.test import APIClient

from core.response import Response
from core.testcase import TestCase


class SignupTest(TestCase):
    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=True)
        self.username = 'nc@notecloud-test.com'
        self.password = 'password'

    def test_signup_check_duplicate_username(self):
        response = self.post(
            '/api/accounts/signup/',
            {
                'username': self.username,
                'password': self.password,
            }
        )
        assert (
            response.status_code == Response.HTTP_201 and
            self.data.get('username') == self.username
        )

        response = self.post(
            '/api/accounts/signup/',
            {
                'username': self.username,
                'password': self.password,
            }
        )
        assert response.status_code == Response.HTTP_400

    def test_signup_check_no_password(self):
        response = self.post(
            '/api/accounts/signup/',
            {
                'username': self.username,
            }
        )
        assert response.status_code == Response.HTTP_400

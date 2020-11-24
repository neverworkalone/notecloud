from core.response import Response
from core.testcase import TestCase


class ProfileTest(TestCase):
    def setUp(self):
        self.create_user()

    def test_connect(self):
        response = self.post(
            '/api/accounts/connect/',
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            self.data.get('key') == self.key and
            self.data.get('user').get('username') == self.user.username
        )

    def test_get_profile(self):
        response = self.get(
            '/api/accounts/setting/',
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            self.data.get('username') == self.user.username and
            self.data.get('is_approved') == self.user.is_approved
        )

    def test_update_profile(self):
        response = self.patch(
            '/api/accounts/setting/',
            {
                'username': 'b-boy@b.com',
                'is_approved': not self.user.is_approved,
            },
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            self.data.get('username') == self.user.username and
            self.data.get('is_approved') == self.user.is_approved
        )

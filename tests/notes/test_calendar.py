from core.response import Response
from core.testcase import TestCase

from accounts.models import User
from notes.models import Task


class TaskCalendar(TestCase):
    def setUp(self):
        self.create_user()

    def test_calendar_spy(self):
        owner = User.objects.create_user(
            username='2@a.com',
            password='password',
            is_approved=True,
        )
        Task.objects.create(
            owner=owner,
            content='Do not spy me',
            date='2020-12-24',
        )

        response = self.get(
            '/api/notes/tasks/?date=2020-12-24',
            auth=True
        )

        assert (
            response.status_code == Response.HTTP_200 and
            not self.data.get('tasks')
        )

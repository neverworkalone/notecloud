from django.conf import settings
from django.utils import timezone

from core.response import Response
from core.testcase import TestCase

from accounts.models import User
from notes.models import Task
from notes import tools


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
            date_from='2020-12-24',
        )

        response = self.get(
            '/api/notes/tasks/?date=2020-12-24',
            auth=True
        )

        assert (
            response.status_code == Response.HTTP_200 and
            not self.data[0].get('tasks')
        )

    def test_calendar_first_weekday(self):
        today = timezone.now().date()
        first_weekday = tools.get_first_weekday(today)

        if settings.FIRST_WEEKDAY_SUNDAY:
            assert first_weekday.weekday() == 6
        else:
            assert first_weekday.weekday() == 0

    def test_calendar_date_and_weekday(self):
        today = timezone.now().date()
        first_weekday = tools.get_first_weekday(today)
        week_ago = first_weekday - timezone.timedelta(1)
        week_later = first_weekday + timezone.timedelta(7)

        self.create_task()

        response = self.get(
            '/api/notes/tasks/',
            auth=True
        )

        pagination = response.data.get('pagination')
        calendar = self.data

        if settings.FIRST_WEEKDAY_SUNDAY:
            weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        else:
            weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

        for index, day in enumerate(calendar):
            assert (
                day.get('weekday') == weekdays[index] and
                day.get('date') == first_weekday + timezone.timedelta(index)
            )

        assert (
            pagination.get('date_before') == week_ago and
            pagination.get('date_after') == week_later and
            pagination.get('date_current') == first_weekday and
            pagination.get('today') == today
        )

    def test_calendar_tasks_by_date(self):
        today = timezone.now().date()
        first_weekday = tools.get_first_weekday(today)
        week_ago = first_weekday - timezone.timedelta(1)

        self.create_task(date_from=week_ago)

        response = self.get(
            '/api/notes/tasks/',
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            self.data[0].get('tasks') and
            self.data[0].get('tasks')[0].get('id') == self.task.id
        )

        long_ago = week_ago - timezone.timedelta(10)

        response = self.get(
            '/api/notes/tasks/?date=%s' % long_ago,
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            not self.data[6].get('tasks')
        )

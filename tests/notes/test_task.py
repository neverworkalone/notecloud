from django.conf import settings

from core.response import Response
from core.testcase import TestCase

from utils.constants import Const

from accounts.models import User
from notes.models import Task


class TaskCreateTest(TestCase):
    def setUp(self):
        self.create_user()

    def test_task_new_basic(self):
        response = self.post(
            '/api/notes/task/new/',
            {
                'date_from': '2020-12-25',
                'date_until': '2020-12-31',
                'content': 'Test',
                'color': 'black',
                'is_completed': True,
                'is_deleted': True,
            },
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_201 and
            self.data.get('date_from') == '2020-12-25' and
            self.data.get('content') == 'Test' and
            self.data.get('color') == 'black' and
            not self.data.get('date_until') and
            not self.data.get('is_completed') and
            not self.data.get('is_deleted')
        )

    def test_task_new_default_color(self):
        response = self.post(
            '/api/notes/task/new/',
            {
                'date_from': '2020-12-01',
                'content': 'Test',
            },
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_201 and
            self.data.get('color') == Const.TASK_COLOR_DEFAULT
        )


class TaskUpdateTest(TestCase):
    def setUp(self):
        self.create_user()
        self.create_task()

    def test_task_spy_task(self):
        owner = User.objects.create_user(
            username='2@a.com',
            password='password',
            is_approved=True,
        )
        task = Task.objects.create(
            owner=owner,
            content='Do not spy me',
            date_from='2020-12-24',
        )

        response = self.patch(
            '/api/notes/task/%d/' % task.id,
            {
                'color': 'white'
            }
        )
        assert response.status_code == Response.HTTP_401

        response = self.delete(
            '/api/notes/task/%d/' % task.id,
        )
        assert response.status_code == Response.HTTP_401

        response = self.post(
            '/api/notes/task/%d/complete/' % task.id,
        )
        assert response.status_code == Response.HTTP_401

        response = self.patch(
            '/api/notes/task/%d/' % task.id,
            {
                'color': 'white'
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_404

        response = self.delete(
            '/api/notes/task/%d/' % task.id,
            auth=True
        )
        assert response.status_code == Response.HTTP_404

        response = self.post(
            '/api/notes/task/%d/complete/' % task.id,
            auth=True
        )
        assert response.status_code == Response.HTTP_404

    def test_task_update(self):
        response = self.patch(
            '/api/notes/task/%d/' % self.task.id,
            {
                'date_from': '2020-12-25',
                'content': 'Boxing',
                'color': 'black',
                'is_completed': not self.task.is_completed,
                'is_deleted': not self.task.is_deleted,
            },
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            self.data.get('date_from') == '2020-12-25' and
            self.data.get('content') == 'Boxing' and
            self.data.get('color') == 'black' and
            self.data.get('is_completed') == self.task.is_completed and
            self.data.get('is_deleted') == self.task.is_deleted
        )

    def test_task_toggle_complete(self):
        response = self.post(
            '/api/notes/task/%d/complete/' % self.task.id,
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            self.data.get('date_until') and
            self.data.get('is_completed') != self.task.is_completed
        )
        response = self.post(
            '/api/notes/task/%d/complete/' % self.task.id,
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            not self.data.get('date_until') and
            self.data.get('is_completed') == self.task.is_completed
        )

    def test_task_delete(self):
        response = self.delete(
            '/api/notes/task/%d/' % self.task.id,
            auth=True
        )
        assert response.status_code == Response.HTTP_204


class TaskListTest(TestCase):
    def setUp(self):
        self.create_user()
        self.create_task()

    def test_task_list_all_completed(self):
        task = Task.objects.create(
            owner=self.user,
            content='Boxing day',
            color="white",
            date_from='2020-12-25',
        )

        self.post(
            '/api/notes/task/%d/complete/' % self.task.id,
            auth=True
        )
        response = self.get(
            '/api/notes/tasks/?date=' + self.task.date_from,
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            self.data.get('calendar')[6].get('count') == 2 and
            self.data.get('calendar')[6].get('incompleted_exist') and
            not self.data.get('calendar')[6].get('all_completed')
        )

        if settings.FIRST_WEEKDAY_SUNDAY:
            index = 4
        else:
            index = 3
        assert (
            self.data.get('calendar')[index].get('count') == 1 and
            self.data.get('calendar')[index].get('all_completed') and
            not self.data.get('calendar')[index].get('incompleted_exist')
        )
        assert (
            self.data.get('calendar')[index - 1].get('count') == 0 and
            not self.data.get('calendar')[index - 1].get('all_completed') and
            not self.data.get('calendar')[index - 1].get('incompleted_exist')
        )

        self.post(
            '/api/notes/task/%d/complete/' % task.id,
            auth=True
        )
        response = self.get(
            '/api/notes/tasks/?date=' + task.date_from,
            auth=True
        )
        assert (
            self.data.get('calendar')[index + 1].get('count') == 2 and
            self.data.get('calendar')[index + 1].get('all_completed') and
            not self.data.get('calendar')[index + 1].get('incompleted_exist')
        )


class TaskSearchTest(TestCase):
    def setUp(self):
        self.create_user(is_prime=True)

    def test_search_tasks(self):
        tasks = [
            {
                'id': 0,
                'content': 'key ab',
                'date_from': '2020-12-24',
                'search': True,
                'complete': True,
            },
            {
                'id': 0,
                'content': 'ke ab',
                'date_from': '2020-12-25',
                'search': False,
                'complete': True,
            },
            {
                'id': 0,
                'content': 'Keyab',
                'date_from': '2020-12-26',
                'search': True,
                'complete': False,
            },
            {
                'id': 0,
                'content': '12kEYab',
                'date_from': '2020-12-27',
                'search': True,
                'complete': False,
            },
            {
                'id': 0,
                'content': 'Ceyab',
                'date_from': '2020-12-28',
                'search': False,
                'complete': False,
            },
            {
                'id': 0,
                'content': 'KEY',
                'date_from': '2020-12-29',
                'search': True,
                'complete': False,
            },
            {
                'id': 0,
                'content': 'k e y',
                'date_from': '2020-12-30',
                'search': False,
                'complete': False,
            },
        ]
        search_list = []

        for index, task in enumerate(tasks):
            instance = self.create_task(
                content=task.get('content'),
                date_from=task.get('date_from')
            )
            tasks[index]['id'] = instance.id

            if task.get('search'):
                search_list.append(instance.id)

            if task.get('complete'):
                response = self.post(
                    '/api/notes/task/%d/complete/' % instance.id,
                    auth=True
                )
                assert response.status_code == Response.HTTP_200

        response = self.get(
            '/api/notes/tasks/search/?q=key',
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            len(self.data) == len(search_list)
        )
        for data in self.data:
            assert int(data.get('id')) in search_list

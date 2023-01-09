from core.response import Response
from core.testcase import TestCase

from utils.constants import Const


class QuestionCreateTest(TestCase):
    def setUp(self):
        self.create_user()

    def test_question_by_anonymouse(self):
        response = self.post(
            '/api/forums/question/new/',
            {
                'address': '1@a.com',
                'title': 'title',
                'content': 'content',
            }
        )
        assert (
            response.status_code == Response.HTTP_201 and
            self.data.get('address') == '1@a.com' and
            self.data.get('title') == 'title' and
            self.data.get('content') == 'content'
        )

        response = self.post(
            '/api/forums/question/new/',
            {
                'title': 'title',
                'content': 'content',
            }
        )
        assert (
            response.status_code == Response.HTTP_201 and
            not self.data.get('address') and
            self.data.get('title') == 'title' and
            self.data.get('content') == 'content'
        )

        response = self.post(
            '/api/forums/question/new/',
            {
                'content': 'content',
            }
        )
        assert response.status_code == Response.HTTP_400

        response = self.get(
            '/api/forums/questions/'
        )
        assert response.status_code == Response.HTTP_401

    def test_question_by_user(self):
        response = self.post(
            '/api/forums/question/new/',
            {
                'title': 'title',
                'content': 'content',
            },
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_201 and
            self.data.get('user') == self.user.id and
            self.data.get('title') == 'title' and
            self.data.get('content') == 'content' and
            not self.data.get('address')
        )

        response = self.get(
            '/api/forums/question/%d/' % self.data.get('id'),
            auth=True
        )
        assert response.status_code == Response.HTTP_403

        response = self.post(
            '/api/forums/question/new/',
            {
                'address': '2@a.com',
                'title': 'title',
                'content': 'content',
            },
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_201 and
            self.data.get('user') == self.user.id and
            self.data.get('title') == 'title' and
            self.data.get('content') == 'content' and
            self.data.get('address') == '2@a.com'
        )

        response = self.get(
            '/api/forums/questions/',
            auth=True

        )
        assert response.status_code == Response.HTTP_403


class QuestionManageTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)
        self.create_question()

    def test_question_by_staff(self):
        response = self.get(
            '/api/forums/questions/',
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            not self.data[0].get('assignee') and
            not self.data[0].get('answer') and
            self.data[0].get('user') == self.question.user and
            self.data[0].get('id') == self.question.id and
            self.data[0].get('title') == self.question.title and
            self.data[0].get('address') == self.question.address and
            self.data[0].get('state') == Const.QUESTION_STATE_NEW and
            self.data[0].get('date_or_time') == self.question.date_or_time()
        )

        response = self.get(
            '/api/forums/question/%d/' % self.question.id,
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            not self.data.get('assignee') and
            not self.data.get('answer') and
            self.data.get('user') == self.question.user and
            self.data.get('id') == self.question.id and
            self.data.get('title') == self.question.title and
            self.data.get('content') == self.question.content and
            self.data.get('address') == self.question.address and
            self.data.get('state') == Const.QUESTION_STATE_NEW
        )

    def test_question_state_open(self):
        response = self.post(
            '/api/forums/question/%d/answer/' % self.question.id,
            {
                'state': Const.QUESTION_STATE_OPEN,
            },
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            self.data.get('id') == self.question.id and
            not self.data.get('answer') and
            self.data.get('state') == Const.QUESTION_STATE_OPEN and
            self.data.get('updated_at') != self.question.updated_at and
            self.data.get('assignee').get('username') == self.user.username
        )

    def test_question_answer_open(self):
        answer = 'it will be checked later.'
        response = self.post(
            '/api/forums/question/%d/answer/' % self.question.id,
            {
                'state': Const.QUESTION_STATE_OPEN,
                'answer': answer,
            },
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            self.data.get('id') == self.question.id and
            self.data.get('answer') and
            self.data.get('state') == Const.QUESTION_STATE_OPEN and
            self.data.get('updated_at') != self.question.updated_at and
            self.data.get('assignee').get('username') == self.user.username
        )

    def test_question_state_closed(self):
        response = self.post(
            '/api/forums/question/%d/answer/' % self.question.id,
            {
                'state': Const.QUESTION_STATE_CLOSED,
            },
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            self.data.get('id') == self.question.id and
            not self.data.get('answer') and
            self.data.get('state') == Const.QUESTION_STATE_CLOSED and
            self.data.get('assignee').get('username') == self.user.username
        )

    def test_question_answer_closed(self):
        answer = 'Resolved'
        response = self.post(
            '/api/forums/question/%d/answer/' % self.question.id,
            {
                'state': Const.QUESTION_STATE_CLOSED,
                'answer': answer,
            },
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            self.data.get('id') == self.question.id and
            self.data.get('answer') == answer and
            self.data.get('state') == Const.QUESTION_STATE_CLOSED and
            self.data.get('assignee').get('username') == self.user.username
        )

    def test_question_state_deleted(self):
        answer = 'Spam'
        response = self.post(
            '/api/forums/question/%d/answer/' % self.question.id,
            {
                'state': Const.QUESTION_STATE_DELETED,
                'answer': answer,
            },
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            self.data.get('id') == self.question.id and
            self.data.get('answer') == answer and
            self.data.get('state') == Const.QUESTION_STATE_DELETED and
            self.data.get('assignee').get('username') == self.user.username
        )


class QuestionListTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)

    def test_question_filtered_list(self):
        questions = [
            {
                'id': 0,
                'title': 'new 1',
                'content': 'new 1',
                'state': Const.QUESTION_STATE_NEW,
            },
            {
                'id': 0,
                'title': 'new 2',
                'content': 'new 2',
                'state': Const.QUESTION_STATE_NEW,
            },
            {
                'id': 0,
                'title': 'open 2',
                'content': 'open 1',
                'state': Const.QUESTION_STATE_OPEN,
            },
            {
                'id': 0,
                'title': 'closed 1',
                'content': 'closed 2',
                'state': Const.QUESTION_STATE_CLOSED,
            },
            {
                'id': 0,
                'title': 'deleted 1',
                'content': 'deleted 2',
                'state': Const.QUESTION_STATE_DELETED,
            }
        ]
        new_list = []
        open_list = []
        closed_list = []
        deleted_list = []

        for index, question in enumerate(questions):
            instance = self.create_question(
                title=question.get('title'),
                content=question.get('content'),
            )
            questions[index]['id'] = instance.id

            if not question.get('state') == Const.QUESTION_STATE_NEW:
                self.post(
                    '/api/forums/question/%d/answer/' % instance.id,
                    {
                        'state': question.get('state'),
                    },
                    auth=True
                )

            if question.get('state') == Const.QUESTION_STATE_OPEN:
                open_list.append(instance.id)
            elif question.get('state') == Const.QUESTION_STATE_CLOSED:
                closed_list.append(instance.id)
            elif question.get('state') == Const.QUESTION_STATE_DELETED:
                deleted_list.append(instance.id)
            else:
                new_list.append(instance.id)

        response = self.get(
            '/api/forums/questions/?state=%s' % (
                Const.QUESTION_STATE_NEW
            ),
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            len(self.data) == len(new_list)
        )
        for data in self.data:
            assert int(data.get('id')) in new_list

        response = self.get(
            '/api/forums/questions/?state=%s' % (
                Const.QUESTION_STATE_OPEN
            ),
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            len(self.data) == len(open_list)
        )
        for data in self.data:
            assert data.get('id') in open_list

        response = self.get(
            '/api/forums/questions/?state=%s' % (
                Const.QUESTION_STATE_CLOSED
            ),
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            len(self.data) == len(closed_list)
        )
        for data in self.data:
            assert data.get('id') in closed_list

        response = self.get(
            '/api/forums/questions/?q=new',
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            len(self.data) == len(new_list)
        )
        for data in self.data:
            assert data.get('id') in new_list

        response = self.get(
            '/api/forums/questions/?q=1&state=new',
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            len(self.data) == 1 and
            self.data[0].get('id') == questions[0].get('id')
        )

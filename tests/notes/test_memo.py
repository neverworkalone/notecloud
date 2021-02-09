from core.response import Response
from core.testcase import TestCase


class MemoCreateTest(TestCase):
    def setUp(self):
        self.create_user()

    def test_memo_new_permission(self):
        response = self.post(
            '/api/notes/memo/new/',
            {
                'title': 'test',
                'content': 'content',
            },
            auth=True
        )
        assert response.status_code == Response.HTTP_403


class MemoTestByPrime(TestCase):
    def setUp(self):
        self.create_user(is_prime=True)

    def test_memo_new_basic(self):
        response = self.post(
            '/api/notes/memo/new/',
            {
                'title': 'test',
                'content': 'content',
            },
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_201 and
            self.data.get('title') == 'test' and
            self.data.get('content') == 'content'
        )


class MemoUpdateTest(TestCase):
    def setUp(self):
        self.create_user(is_prime=True)
        self.create_memo()

    def test_memo_update(self):
        response = self.patch(
            '/api/notes/memo/%d/' % self.memo.id,
            {
                'title': 'no test',
            },
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            self.data.get('title') == 'no test' and
            self.data.get('content') == self.memo.content
        )

        response = self.patch(
            '/api/notes/memo/%d/' % self.memo.id,
            {
                'title': 'test',
                'content': 'no content',
            },
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            self.data.get('title') == 'test' and
            self.data.get('content') == 'no content'
        )

    def test_memo_delete(self):
        response = self.delete(
            '/api/notes/memo/%d/' % self.memo.id,
            auth=True
        )
        assert response.status_code == Response.HTTP_204

        response = self.get(
            '/api/notes/memos/',
            auth=True
        )
        assert not self.data


class MemoListTest(TestCase):
    def setUp(self):
        self.create_user(is_prime=True)

    def test_memo_list(self):
        sample_title = [
            'black',
            'white',
            'red',
            'blue',
            'purple',
        ]
        sample_content = [
            'cat',
            'rabbit',
            'eagle',
            'pig',
            'chicken',
        ]
        memo_list = []
        for index in range(5):
            memo = self.create_memo(
                title=sample_title[index],
                content=sample_content[index]
            )
            memo_list.append(memo)

        self.get(
            '/api/notes/memos/?page=1&page_size=10',
            auth=True
        )

        for index, memo in enumerate(reversed(memo_list)):
            assert (
                memo.id == self.data[index].get('id') and
                memo.title == self.data[index].get('title')
            )

        for index, memo in enumerate(reversed(memo_list)):
            response = self.get(
                '/api/notes/memo/%d/' % memo.id,
                auth=True
            )
            assert (
                response.status_code == Response.HTTP_200 and
                self.data.get('title') == memo.title and
                self.data.get('content') == memo.content
            )

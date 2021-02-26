import datetime
from django.conf import settings
from django.utils import timezone

from core.response import Response
from core.testcase import TestCase

from utils.constants import Const

from notes.models import Memo


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

    def test_memo_updated_at(self):
        yesterday = timezone.now() - timezone.timedelta(1)
        memo = Memo.objects.create(
            owner=self.user,
            title='test',
            content='content',
            doctype='text',
            updated_at=yesterday
        )

        response = self.get(
            '/api/notes/memo/%d/' % memo.id,
            auth=True
        )
        response = self.patch(
            '/api/notes/memo/%d/' % memo.id,
            {
                'content': 'no content',
            },
            auth=True
        )
        updated_at = datetime.datetime.strptime(
            self.data.get('updated_at'),
            settings.DATE_TIME_FORMAT_DEFAULT
        )
        self.log(updated_at, yesterday)
        assert (
            response.status_code == Response.HTTP_200 and
            self.data.get('content') == 'no content' and
            updated_at > yesterday
        )


class MemoTrashTest(TestCase):
    def setUp(self):
        self.create_user(is_prime=True)
        self.create_memo()

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

    def test_memo_trash(self):
        memo_list = []
        for index in range(5):
            memo = self.create_memo()
            memo_list.append(memo)

            self.delete(
                '/api/notes/memo/%d/' % memo.id,
                auth=True
            )

        self.get(
            '/api/notes/memos/trash/',
            auth=True
        )
        for index, memo in enumerate(reversed(memo_list)):
            assert (
                memo.id == self.data[index].get('id') and
                memo.title == self.data[index].get('title')
            )

        self.post(
            '/api/notes/memo/%d/restore/' % memo_list[0].id,
            auth=True
        )
        self.get(
            '/api/notes/memos/trash/',
            auth=True
        )
        assert (
            len(self.data) == 4
        )

        response = self.post(
            '/api/notes/memos/trash/empty/',
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_204
        )
        response = self.get(
            '/api/notes/memos/trash/',
            auth=True
        )
        assert (
            not len(self.data)
        )


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

        response = self.get(
            '/api/notes/memos/?page=1&page_size=10&q=p',
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            len(self.data) == 2
        )
        for data in self.data:
            assert (
                data.get('title') == 'blue' or
                data.get('title') == 'purple'
            )


class MemoShareTest(TestCase):
    def setUp(self):
        self.create_user(is_prime=True)
        self.create_memo()

    def test_memo_yet_shared(self):
        response = self.get(
            '/api/notes/memo/shared/%d/' % self.memo.id
        )
        assert (
            response.status_code == Response.HTTP_404
        )

        response = self.get(
            '/api/notes/memos/shared/',
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            not len(self.data)
        )

        response = self.get(
            '/api/notes/memo/shared/%d/' % self.memo.id,
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_404
        )

    def test_memo_shared(self):
        response = self.post(
            '/api/notes/memo/%d/share/' % self.memo.id,
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            self.data.get('is_shared')
        )

        response = self.get(
            '/api/notes/memos/shared/'
        )
        assert (
            response.status_code == Response.HTTP_401
        )

        response = self.get(
            '/api/notes/memos/shared/',
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            len(self.data) == 1 and
            self.data[0].get('id') == self.memo.id and
            self.data[0].get('date_or_time') == self.memo.date_or_time()
        )

        response = self.get(
            '/api/notes/memo/shared/%d/' % self.memo.id
        )
        assert (
            response.status_code == Response.HTTP_200 and
            self.data.get('title') and
            self.data.get('content')
        )

        response = self.post(
            '/api/notes/memo/%d/unshare/' % self.memo.id,
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            not self.data.get('is_shared')
        )

        response = self.get(
            '/api/notes/memos/shared/',
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            len(self.data) == 0
        )

    def test_memo_delete_shared(self):
        self.patch(
            '/api/notes/memo/%d/' % self.memo.id,
            {
                'is_shared': True,
            },
            auth=True
        )
        self.delete(
            '/api/notes/memo/%d/' % self.memo.id,
            auth=True
        )
        response = self.get(
            '/api/notes/memo/shared/%d/' % self.memo.id
        )
        assert (
            response.status_code == Response.HTTP_404
        )

        response = self.post(
            '/api/notes/memo/%d/restore/' % self.memo.id,
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            not self.data.get('is_shared')
        )


class MemoPinnedTest(TestCase):
    def setUp(self):
        self.create_user(is_prime=True)
        self.create_memo()

    def test_memo_yet_pinned(self):
        response = self.get(
            '/api/notes/memos/pinned/',
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            not len(self.data)
        )

    def test_memo_pinned(self):
        response = self.post(
            '/api/notes/memo/%d/pin/' % self.memo.id,
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            self.data.get('is_pinned')
        )

        response = self.get(
            '/api/notes/memos/pinned/'
        )
        assert (
            response.status_code == Response.HTTP_401
        )

        response = self.get(
            '/api/notes/memos/pinned/',
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            len(self.data) == 1 and
            self.data[0].get('id') == self.memo.id and
            self.data[0].get('date_or_time') == self.memo.date_or_time()
        )

        response = self.post(
            '/api/notes/memo/%d/unpin/' % self.memo.id,
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            not self.data.get('is_pinned')
        )

        response = self.get(
            '/api/notes/memos/pinned/',
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            len(self.data) == 0
        )

    def test_memo_delete_pinned(self):
        self.patch(
            '/api/notes/memo/%d/' % self.memo.id,
            {
                'is_pinned': True,
            },
            auth=True
        )
        self.delete(
            '/api/notes/memo/%d/' % self.memo.id,
            auth=True
        )

        response = self.get(
            '/api/notes/memos/pinned/',
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            not len(self.data)
        )

        response = self.post(
            '/api/notes/memo/%d/restore/' % self.memo.id,
            auth=True
        )
        assert (
            response.status_code == Response.HTTP_200 and
            not self.data.get('is_pinned')
        )


class MemoDocTypeTest(TestCase):
    def setUp(self):
        self.create_user(is_prime=True)

    def test_memo_doctype_code(self):
        self.post(
            '/api/notes/memo/new/',
            {
                'title': 'code',
                'content': Const.DOCTYPE_CODE
            },
            auth=True
        )
        assert self.data.get('doctype') == 'code'

    def test_memo_doctype_table(self):
        self.post(
            '/api/notes/memo/new/',
            {
                'title': 'table',
                'content': Const.DOCTYPE_TABLE
            },
            auth=True
        )
        assert self.data.get('doctype') == 'table'

    def test_memo_doctype_bullet(self):
        self.post(
            '/api/notes/memo/new/',
            {
                'title': 'bullet',
                'content': Const.DOCTYPE_BULLET
            },
            auth=True
        )
        assert self.data.get('doctype') == 'bullet'

    def test_memo_doctype_order(self):
        self.post(
            '/api/notes/memo/new/',
            {
                'title': 'order',
                'content': Const.DOCTYPE_ORDER
            },
            auth=True
        )
        assert self.data.get('doctype') == 'order'

    def test_memo_doctype_mix(self):
        content = '%s%s%s%s' % (
            '<ol><li>order</li></ol>',
            '<ul><li>bullet</li></ul>',
            '<table><tr><td>table</td></tr></table>',
            '<pre><code>import datetime</code></pre>'
        )
        self.post(
            '/api/notes/memo/new/',
            {
                'title': 'mix',
                'content': content
            },
            auth=True
        )
        assert self.data.get('doctype') == 'code'

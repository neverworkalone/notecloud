import threading

import accounts
import notes

from django.utils import timezone

from core.permissions import IsAdminUser
from core.response import Response
from core.viewsets import APIView

from utils.constants import Const
from utils.debug import Debug  # noqa


class BotView(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request, *args, **kwargs):
        daily_task()
        return Response(status=Response.HTTP_200)


def run_thread(target):
    thread = threading.Thread(target=target)
    thread.start()


def check_expired_prime(today):
    users = accounts.models.User.objects.prime()

    for user in users:
        if not user.prime_until or user.prime_until <= today:
            Debug.trace(
                'Prime expired for user(%d)' % user.id
            )
            user.is_prime = False
            user.save(update_fields=['is_prime'])


def check_expired_memo_in_trash(now):
    retard = now - timezone.timedelta(Const.TRASH_KEEP_DAYS)
    expired_trashes = notes.models.Memo.objects.expired_trash(retard)
    trash_list = []

    for trash in expired_trashes:
        trash_list.append(trash.id)

    if expired_trashes:
        Debug.trace(
            'Delete expired trashes %s' % trash_list
        )
        expired_trashes.delete()


def daily_task():
    now = timezone.now()
    today = now.date()

    Debug.trace(
        'Staring %s daily task...' % today
    )

    check_expired_prime(today)
    check_expired_memo_in_trash(now)

    Debug.trace(
        '%s daily task finished.' % today
    )


def bot_daily():
    run_thread(daily_task)

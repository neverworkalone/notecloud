from django.conf import settings
from django.utils import timezone

from utils.constants import Const
from utils.debug import Debug  # noqa


def toggle_complete(task):
    task.is_completed = not task.is_completed
    if task.is_completed:
        task.date_until = timezone.localtime(timezone.now()).date()
    else:
        task.date_until = None

    task.save(update_fields=['is_completed', 'date_until'])


def delete_task(task):
    task.is_deleted = True
    task.save(update_fields=['is_deleted'])


def get_first_weekday(date):
    if settings.FIRST_WEEKDAY_SUNDAY:
        if date.isoweekday() == 7:
            delta = 0
        else:
            delta = date.isoweekday()
    else:
        delta = date.weekday()

    first_weekday = date - timezone.timedelta(delta)
    return first_weekday


def get_date_pagination(first_weekday):
    date_before = first_weekday - timezone.timedelta(1)
    date_after = first_weekday + timezone.timedelta(7)
    return date_before.date(), date_after.date()


def get_weekday_text(weekday):
    weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    return weekdays[weekday]


def get_weekly_calendar(first_weekday):
    calendar = []

    for index in range(0, 7):
        date = first_weekday + timezone.timedelta(index)
        data = {
            'date': date.date(),
            'weekday': get_weekday_text(date.weekday())
        }
        calendar.append(data)

    return calendar


def delete_memo(memo):
    if not memo.is_deleted:
        memo.is_deleted = True
        memo.is_pinned = False
        memo.is_shared = False
        memo.updated_at = timezone.now()
        memo.save(
            update_fields=[
                'is_deleted',
                'is_pinned',
                'is_shared',
                'updated_at'
            ]
        )


def restore_memo(memo):
    if memo.is_deleted:
        memo.is_deleted = False
        memo.updated_at = timezone.now()
        memo.save(update_fields=['is_deleted', 'updated_at'])


def pin_memo(memo, unpin=False):
    memo.is_pinned = not unpin
    memo.save(update_fields=['is_pinned'])


def share_memo(memo, unshare=False):
    memo.is_shared = not unshare
    memo.save(update_fields=['is_shared'])


def get_doctype(content):
    if Const.DOCTYPE_CODE in content:
        return 'code'
    elif Const.DOCTYPE_TABLE in content:
        return 'table'
    elif Const.DOCTYPE_BULLET in content:
        return 'bullet'
    elif Const.DOCTYPE_ORDER in content:
        return 'order'
    else:
        return 'doc'

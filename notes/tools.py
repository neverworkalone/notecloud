from django.conf import settings
from django.utils import timezone

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

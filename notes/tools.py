from django.conf import settings
from django.utils import timezone

from utils.debug import Debug  # noqa


def toggle_complete(task):
    task.is_completed = not task.is_completed
    task.save(update_fields=['is_completed'])


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
    if weekday == 0:
        text = 'Mon'
    elif weekday == 1:
        text = 'Tue'
    elif weekday == 2:
        text = 'Wed'
    elif weekday == 3:
        text = 'Thu'
    elif weekday == 4:
        text = 'Fri'
    elif weekday == 5:
        text = 'Sat'
    elif weekday == 6:
        text = 'Sun'

    return text


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

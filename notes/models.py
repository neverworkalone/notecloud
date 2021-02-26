from django.db import models
from django.db.models import Q
from django.utils import timezone

from utils.constants import Const
from utils.debug import Debug  # noqa


class TaskManager(models.Manager):
    def my(self, user):
        return self.filter(owner=user).filter(is_deleted=False)

    def search(self, user, q):
        if q:
            return self.my(user).filter(content__icontains=q)
        else:
            return self.none()

    def my_completed(self, user):
        return self.my(user).filter(is_completed=True)

    def my_ongoing(self, user):
        return self.my(user).filter(is_completed=False)

    def today_tasks(self, user, date=None):
        if not date:
            date = timezone.now()

        tasks = (
            Q(date_from__lte=date.date()) &
            (
                Q(is_completed=False) |
                (
                    Q(is_completed=True) &
                    Q(date_until__gte=date.date())
                )
            )
        )
        return self.my(user).filter(tasks).order_by(
            '-is_completed', 'date_from', 'id'
        )


class Task(models.Model):
    owner = models.ForeignKey(
        'accounts.User',
        related_name='task_owner',
        on_delete=models.CASCADE,
        null=True,
    )
    content = models.CharField(
        max_length=Const.DESC_MAX_LENGTH,
        blank=True,
        null=True,
    )
    color = models.CharField(
        max_length=Const.COLOR_MAX_LENGTH,
        blank=True,
        null=True,
    )
    date_from = models.DateField(blank=True, null=True)
    date_until = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_completed = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    objects = TaskManager()

    class Meta:
        ordering = ('date_from', 'id',)


class MemoManager(models.Manager):
    def my(self, user):
        return self.filter(owner=user).filter(is_deleted=False)

    def my_trash(self, user):
        return self.filter(owner=user).filter(is_deleted=True)

    def my_pinned(self, user):
        return self.my(user).filter(is_pinned=True)

    def my_shared(self, user):
        return self.my(user).filter(is_shared=True)

    def shared(self):
        return self.filter(is_deleted=False).filter(is_shared=True)


class Memo(models.Model):
    owner = models.ForeignKey(
        'accounts.User',
        related_name='memo_owner',
        on_delete=models.CASCADE,
        null=True,
    )
    title = models.CharField(
        max_length=Const.TITLE_MAX_LENGTH,
        blank=True,
        null=True,
    )
    content = models.TextField(
        blank=True,
        null=True,
    )
    updated_at = models.DateTimeField(default=timezone.now)
    doctype = models.CharField(
        max_length=Const.MEMO_TYPE_MAX_LENGTH,
        blank=True,
        null=True,
    )
    is_pinned = models.BooleanField(default=False)
    is_shared = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    objects = MemoManager()

    class Meta:
        ordering = ('-updated_at',)

    def date_or_time(self):
        today = timezone.localtime(timezone.now())
        updated_at = timezone.localtime(self.updated_at)

        if updated_at.date() == today.date():
            return {
                'date': None,
                'time': updated_at.time().strftime(Const.TIME_FORMAT_DEFAULT),
            }
        else:
            return {
                'date': updated_at.date(),
                'time': None,
            }

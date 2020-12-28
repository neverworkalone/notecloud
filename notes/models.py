from django.db import models
from django.db.models import Q
from django.utils import timezone

from utils.constants import Const
from utils.debug import Debug  # noqa


class TaskManager(models.Manager):
    def my(self, user):
        return self.filter(owner=user).filter(is_deleted=False)

    def weekly_tasks(self, user, first_weekday):
        last_weekday = first_weekday + timezone.timedelta(6)
        date_range = (
            Q(date_from__gte=first_weekday) & Q(date_from__lte=last_weekday)
        )
        return self.my(user).filter(date_range)


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
        ordering = ('date_from', 'id')


class MemoManager(models.Manager):
    pass


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
    is_deleted = models.BooleanField(default=False)

    objects = MemoManager()

    class Meta:
        ordering = ('-id',)

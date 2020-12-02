from django.db import models
from django.utils import timezone

from utils.constants import Const


class TaskManager(models.Manager):
    def my(self, user):
        return self.filter(owner=user).filter(is_deleted=False)


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
    date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_completed = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    objects = TaskManager()

    class Meta:
        ordering = ('-id',)


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

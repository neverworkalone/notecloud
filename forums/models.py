from django.db import models
from django.db.models import Q
from django.utils import timezone

from utils.constants import Const


class QuestionManager(models.Manager):
    def search(self, state, q):
        if q:
            search_query = (
                Q(title__icontains=q) |
                Q(content__icontains=q) |
                Q(answer__icontains=q) |
                Q(address__icontains=q) |
                Q(user__username__icontains=q)
            )
        else:
            search_query = Q()

        if state:
            state_query = Q(state=state)
        else:
            state_query = Q()

        return self.filter(state_query).filter(search_query)


class Question(models.Model):
    user = models.ForeignKey(
        'accounts.User',
        related_name='question_owner',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    assignee = models.ForeignKey(
        'accounts.User',
        related_name='question_assignee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    address = models.CharField(
        max_length=Const.EMAIL_MAX_LENGTH,
        blank=True,
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
    answer = models.TextField(
        blank=True,
        null=True,
    )
    state = models.CharField(
        max_length=Const.LENGTH_32,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    objects = QuestionManager()

    class Meta:
        ordering = ('-updated_at',)

    def date_or_time(self):
        today = timezone.localtime(timezone.now())
        created_at = timezone.localtime(self.created_at)
        updated_at = timezone.localtime(self.updated_at)

        if created_at.date() == today.date():
            created = {
                'date': None,
                'time': created_at.time().strftime(Const.TIME_FORMAT_DEFAULT),
            }
        else:
            created = {
                'date': updated_at.date(),
                'time': None,
            }

        if updated_at.date() == today.date():
            updated = {
                'date': None,
                'time': updated_at.time().strftime(Const.TIME_FORMAT_DEFAULT),
            }
        else:
            updated = {
                'date': updated_at.date(),
                'time': None,
            }

        return {
            'created': created,
            'updated': updated,
        }

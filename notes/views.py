import datetime

from django.conf import settings
from django.db.models import Q
from django.utils import timezone

from core.permissions import (
    AllowAny,
    IsApproved,
    IsPrime,
)
from core.response import (
    PaginatedResponse,
    Response,
)
from core.viewsets import (
    ModelViewSet,
    ReadOnlyModelViewSet,
)

from utils.constants import Const
from utils.debug import Debug  # noqa

from . import (
    models,
    serializers,
    tools,
)


class TaskViewSet(ModelViewSet):
    serializer_class = serializers.TaskSerializer
    model = models.Task

    def get_permissions(self):
        permission_classes = [IsApproved]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return self.model.objects.my(self.request.user)

    def perform_delete(self, instance):
        tools.delete_task(instance)

    def complete(self, request, *args, **kwargs):
        instance = self.get_object()
        tools.toggle_complete(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class TaskListViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.TaskSerializer
    model = models.Task

    def get_permissions(self):
        permission_classes = [IsApproved]
        return [permission() for permission in permission_classes]

    def get_queryset(self, date):
        return self.model.objects.today_tasks(self.request.user, date)

    def get_calendar(self, first_weekday):
        calendar = []

        for index in range(0, 7):
            date = first_weekday + timezone.timedelta(index)
            tasks = self.get_queryset(date)

            incompleted_exist = tasks.filter(is_completed=False).exists()
            completed_exist = tasks.filter(is_completed=True).exists()
            all_completed = bool(completed_exist and not incompleted_exist)

            data = {
                'date': date.date(),
                'weekday': tools.get_weekday_text(date.weekday()),
                'count': tasks.count(),
                'incompleted_exist': incompleted_exist,
                'all_completed': all_completed,
            }
            calendar.append(data)

        return calendar

    def list(self, request, *args, **kwargs):
        date = request.query_params.get('date')
        today = timezone.localtime(timezone.now())
        if date:
            date = datetime.datetime.strptime(
                date,
                settings.DATE_FORMAT_DEFAULT
            )
        else:
            date = today

        queryset = self.get_queryset(date)
        serializer = self.get_serializer(queryset, many=True)

        first_weekday = tools.get_first_weekday(date)
        date_before, date_after = tools.get_date_pagination(first_weekday)

        if date:
            date_current = date
        else:
            date_current = first_weekday

        pagination = {
            'date_before': date_before,
            'date_after': date_after,
            'date_current': date_current.date(),
            'today': today.date(),
        }
        data = {
            'calendar': self.get_calendar(first_weekday),
            'tasks': serializer.data,
        }
        return PaginatedResponse(
            data=data,
            pagination=pagination,
        )


class MemoViewSet(ModelViewSet):
    serializer_class = serializers.MemoSerializer
    model = models.Memo

    def get_permissions(self):
        permission_classes = [IsPrime]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return self.model.objects.my(self.request.user)

    def sync_update(self, instance, partial):
        instance.doctype = tools.get_doctype(instance.content)
        instance.updated_at = timezone.now()

    def perform_delete(self, instance):
        tools.delete_memo(instance)


class MemoTrashViewSet(MemoViewSet):
    def get_queryset(self):
        return self.model.objects.my_trash(self.request.user)

    def restore(self, request, *args, **kwargs):
        instance = self.get_object()
        Debug.trace(
            'Restoring %s' % instance
        )
        tools.restore_memo(instance)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def empty(self, request, *args, **kwargs):
        self.get_queryset().delete()
        return Response(status=Response.HTTP_204)


class MemoListViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.MemoListSerializer
    model = models.Memo

    def get_permissions(self):
        permission_classes = [IsPrime]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        q = self.request.query_params.get(Const.QUERY_PARAM_SEARCH_QUERY)
        if q:
            search_query = (
                Q(title__icontains=q) |
                Q(content__icontains=q)
            )
        else:
            search_query = Q()

        return self.model.objects.my(self.request.user).filter(search_query)


class MemoTrashListViewSet(MemoListViewSet):
    def get_queryset(self):
        return self.model.objects.my_trash(self.request.user)


class SharedMemoListViewSet(MemoListViewSet):
    def get_queryset(self):
        return self.model.objects.my_shared(self.request.user)


class SharedMemoViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.MemoSerializer
    model = models.Memo

    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return self.model.objects.shared()

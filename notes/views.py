import datetime

from django.conf import settings
from django.utils import timezone

from core.permissions import (
    IsApproved,
)
from core.response import (
    PaginatedResponse,
    Response,
)
from core.viewsets import (
    ModelViewSet,
)

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

    def complete(self, request, *args, **kwargs):
        instance = self.get_object()
        tools.toggle_complete(instance)
        serializer = self.set_serializer(
            serializers.TaskCompleteSerializer,
            instance
        )
        return Response(serializer.data)


class TaskListViewSet(TaskViewSet):
    def get_queryset(self, first_weekday):
        return self.model.objects.weekly_tasks(
            self.request.user,
            first_weekday
        )

    def list(self, request, *args, **kwargs):
        today = request.query_params.get('date')
        if today:
            today = datetime.datetime.strptime(
                today,
                settings.DATE_FORMAT_DEFAULT
            )
        else:
            today = timezone.localtime(timezone.now())

        first_weekday = tools.get_first_weekday(today)
        calendar = tools.get_weekly_calendar(first_weekday)
        date_before, date_after = tools.get_date_pagination(first_weekday)

        queryset = self.get_queryset(first_weekday)
        serializer = self.get_serializer(queryset, many=True)

        pagination = {
            'date_before': date_before,
            'date_after': date_after,
            'date_current': first_weekday.date(),
            'today': timezone.localtime(timezone.now()).date(),
        }
        data = {
            'calendar': calendar,
            'tasks': serializer.data,
        }
        return PaginatedResponse(
            data=data,
            pagination=pagination,
        )

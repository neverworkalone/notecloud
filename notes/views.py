import datetime

from django.conf import settings
from django.db.models import Q
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
        return self.model.objects.active_tasks(
            self.request.user,
            first_weekday
        )

    def get_weekly_tasks(self, first_weekday):
        calendar = []
        queryset = self.get_queryset(first_weekday)

        for index in range(0, 7):
            date = first_weekday + timezone.timedelta(index)

            today_tasks = (
                Q(date_from__lte=date.date()) &
                (
                    Q(is_completed=False) |
                    (
                        Q(is_completed=True) &
                        Q(date_until__gte=date.date())
                    )
                )
            )
            tasks = queryset.filter(today_tasks)
            serializer = self.get_serializer(tasks, many=True)

            data = {
                'date': date.date(),
                'weekday': tools.get_weekday_text(date.weekday()),
                'tasks': serializer.data,
            }
            calendar.append(data)

        return calendar

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
        date_before, date_after = tools.get_date_pagination(first_weekday)

        data = self.get_weekly_tasks(first_weekday)

        pagination = {
            'date_before': date_before,
            'date_after': date_after,
            'date_current': first_weekday.date(),
            'today': timezone.localtime(timezone.now()).date(),
        }
        return PaginatedResponse(
            data=data,
            pagination=pagination,
        )

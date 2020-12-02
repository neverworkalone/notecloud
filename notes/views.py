from core.permissions import (
    IsApproved,
)
from core.response import Response
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

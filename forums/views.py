from django.db.models import Q
from django.utils import timezone

from core.permissions import (
    AllowAny,
    IsAdminUser,
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
)


class QuestionViewSet(ModelViewSet):
    serializer_class = serializers.QuestionSerializer
    model = models.Question

    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return self.model.objects.all()


class QuestionAnswerViewSet(QuestionViewSet):
    serializer_class = serializers.QuestionAnswerSerializer

    def get_permissions(self):
        permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def sync_update(self, instance, partial):
        instance.assignee = self.request.user
        instance.updated_at = timezone.now()


class QuestionListViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.QuestionListSerializer
    model = models.Question

    def get_permissions(self):
        permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        q = self.request.query_params.get(Const.QUERY_PARAM_SEARCH)
        state = self.request.query_params.get(Const.QUERY_PARAM_STATE)

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

        return self.model.objects.filter(state_query).filter(search_query)


class QuestionRetrieveViewSet(QuestionListViewSet):
    serializer_class = serializers.QuestionRetrieveSerializer

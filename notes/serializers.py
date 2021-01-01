from core.serializers import (
    ModelSerializer,
)

from utils.constants import Const
from utils.debug import Debug  # noqa

from . import models


class TaskSerializer(ModelSerializer):
    class Meta:
        model = models.Task
        fields = [
            'id',
            'date_from',
            'date_until',
            'color',
            'content',
            'is_completed',
            'is_deleted',
            'created_at',
        ]
        read_only_fields = [
            'id',
            'is_completed',
            'is_deleted',
            'created_at',
        ]
        extra_kwargs = {
            'content': {'required': True},
            'date_from': {'required': True},
        }

    def create(self, validated_data):
        task = self.Meta.model.objects.create(
            owner=self.context.get('request').user,
            content=validated_data.get('content'),
            color=validated_data.get('color', Const.TASK_COLOR_DEFAULT),
            date_from=validated_data.get('date_from'),
        )
        return task

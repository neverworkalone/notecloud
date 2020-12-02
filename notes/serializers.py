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
            'date',
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
            'date': {'required': True},
        }

    def create(self, validated_data):
        task = self.Meta.model.objects.create(
            owner=self.context.get('request').user,
            content=validated_data.get('content'),
            color=validated_data.get('color', Const.TASK_COLOR_DEFAULT),
            date=validated_data.get('date'),
        )
        return task


class TaskCompleteSerializer(ModelSerializer):
    class Meta:
        model = models.Task
        fields = [
            'id',
            'is_completed'
        ]

from core.serializers import (
    ModelSerializer,
)

from utils.constants import Const
from utils.debug import Debug  # noqa

from . import (
    models,
    tools,
)


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


class MemoSerializer(ModelSerializer):
    class Meta:
        model = models.Memo
        fields = [
            'id',
            'title',
            'content',
            'doctype',
            'updated_at',
            'is_shared',
            'is_deleted',
        ]
        read_only_fields = [
            'id',
            'doctype',
            'updated_at',
            'is_deleted',
        ]
        extra_kwargs = {
            'title': {'required': True},
            'content': {'required': True},
        }

    def create(self, validated_data):
        content = validated_data.get('content')
        doctype = tools.get_doctype(content)

        task = self.Meta.model.objects.create(
            owner=self.context.get('request').user,
            title=validated_data.get('title'),
            content=content,
            doctype=doctype,
        )
        return task


class MemoListSerializer(ModelSerializer):
    class Meta:
        model = models.Memo
        fields = [
            'id',
            'title',
            'doctype',
            'date_or_time',
            'is_shared',
            'is_deleted'
        ]

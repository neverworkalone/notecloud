import accounts

from rest_framework import serializers

from core.serializers import (
    ModelSerializer,
)

from utils.constants import Const
from utils.debug import Debug  # noqa
from utils.text import Text

from . import (
    models,
)


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = models.Question
        fields = [
            'id',
            'user',
            'assignee',
            'address',
            'title',
            'content',
            'state',
            'answer',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'user',
            'assignee',
            'state',
            'answer',
            'created_at',
            'updated_at',
        ]
        extra_kwargs = {
            'title': {'required': True},
            'content': {'required': True},
        }

    def create(self, validated_data):
        user = self.context.get('request').user
        if not user.is_authenticated:
            user = None

        question = self.Meta.model.objects.create(
            user=user,
            address=validated_data.get('address'),
            title=validated_data.get('title'),
            content=validated_data.get('content'),
            state=Const.QUESTION_STATE_NEW,
        )
        return question


class QuestionAnswerSerializer(ModelSerializer):
    assignee = accounts.serializers.StaffSerializer()

    class Meta:
        model = models.Question
        fields = [
            'id',
            'assignee',
            'state',
            'answer',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'assignee',
            'updated_at',
        ]

    def validate(self, attrs):
        if attrs.get('state') not in Const.QUESTION_STATE_LIST:
            raise serializers.ValidationError(Text.INVALID_QUESTION_STATE)

        return attrs


class QuestionListSerializer(ModelSerializer):
    user = accounts.serializers.IAmSerializer()

    class Meta:
        model = models.Question
        fields = [
            'id',
            'user',
            'assignee',
            'address',
            'title',
            'state',
            'date_or_time',
        ]


class QuestionRetrieveSerializer(QuestionListSerializer):
    class Meta:
        model = models.Question
        fields = [
            'id',
            'user',
            'assignee',
            'address',
            'title',
            'content',
            'state',
            'answer',
            'created_at',
            'updated_at',
        ]

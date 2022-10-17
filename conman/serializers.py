from rest_framework import serializers
from django.contrib.auth.models import User

from conman.models import CmProcessContext


class StartFormSerializer(serializers.ModelSerializer):
    responsible = serializers.CharField(max_length=50)

    class Meta:
        model = CmProcessContext
        fields = ['short_name', 'what_to_do', 'perform_before', 'responsible']


class ContextSerializer(serializers.ModelSerializer):

    initiator = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )
    responsible = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = CmProcessContext
        fields = ['short_name', 'what_to_do', 'responsible', 'initiator', 'perform_before']


class FinishPlanTaskSerializer(serializers.Serializer):

    task_id = serializers.CharField(max_length=50)
    instance_id = serializers.CharField(max_length=50)
    perform_before = serializers.DateTimeField()


class FinishCompleteTaskSerializer(serializers.Serializer):

    task_id = serializers.CharField(max_length=50)
    instance_id = serializers.CharField(max_length=50)
    perform_before = serializers.DateTimeField(required=False)
    status = serializers.CharField(max_length=12)


class CmProcessInstanceSerializer(serializers.ModelSerializer):

    initiator = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )
    responsible = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = CmProcessContext
        fields = ['short_name', 'responsible', 'initiator', 'perform_before', 'create_date', 'status']

from rest_framework import serializers
from django.contrib.auth.models import User

from conman.models import CmProcessContext


class StartFormSerializer(serializers.ModelSerializer):
    responsible = serializers.CharField(max_length=50)

    class Meta:
        model = CmProcessContext
        fields = ['short_name', 'what_to_do', 'perform_before', 'responsible']

    def create(self, validated_data):
        responsible_user = User.objects.get(username__exact=validated_data.get('responsible'))
        process_context = CmProcessContext.objects.create(
            short_name=validated_data.get('short_name'),
            what_to_do=validated_data.get('what_to_do'),
            perform_before=validated_data.get('perform_before'),
            responsible=responsible_user
        )
        return process_context


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


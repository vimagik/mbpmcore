from rest_framework import serializers

from core.models import TaskModel, ProcessModel


class ProcesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProcessModel
        fields = ['name_ru', 'name_en', 'code', 'id']


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    process = ProcesSerializer(required=False, many=False)

    class Meta:
        model = TaskModel
        fields = ['name', 'process']

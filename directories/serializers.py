from rest_framework import serializers

from directories.models import Meeting


class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    desc = serializers.CharField()
    isTask = serializers.BooleanField()
    responsible = serializers.CharField(allow_blank=True)
    due = serializers.DateField(allow_null=True)


class StartFormMeetingSerializer(serializers.ModelSerializer):

    participants = serializers.ListField()
    tasks = TaskSerializer(many=True, required=False)

    class Meta:
        model = Meeting
        fields = ['name', 'due_of_event', 'description', 'participants', 'tasks']

    def create(self, validated_data):
        new_meeting = Meeting.objects.create(**validated_data)
        return new_meeting

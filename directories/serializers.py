from rest_framework import serializers
from django.contrib.auth.models import User

from directories.models import Meeting, Arrangement


class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    desc = serializers.CharField()
    isTask = serializers.BooleanField()
    responsible = serializers.CharField(allow_blank=True)
    due = serializers.DateField(allow_null=True)


class StartFormMeetingSerializer(serializers.ModelSerializer):

    participants = serializers.ListField(write_only=True)
    tasks = TaskSerializer(many=True, required=False)

    class Meta:
        model = Meeting
        fields = ['name', 'due_of_event', 'description', 'participants', 'tasks']

    def create(self, validated_data):
        new_meeting = Meeting.objects.create(
            name=validated_data['name'],
            due_of_event=validated_data['due_of_event'],
            description=validated_data['description']
        )
        self.add_participants(
            data=validated_data['participants'],
            meeting=new_meeting
            )
        arrangements_data = [val for val in validated_data['tasks'] if val['isTask']==False]
        self.add_arrangements(arrangements_data, new_meeting)
        return new_meeting

    @staticmethod
    def add_participants(data: list, meeting: Meeting) -> None:
        for val in data:
            participant = User.objects.get(username__exact=val)
            meeting.participants.add(participant.id)
    
    @staticmethod
    def add_arrangements(data: list, meeting: Meeting) -> None:
        for val in data:
            Arrangement.objects.create(
                description=val['desc'],
                meeting=meeting,
            )

from rest_framework import serializers
from django.contrib.auth.models import User

from conman.models import CmProcessContext
from directories.models import Meeting, Arrangement
from conman.camunda import create_instance


class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    desc = serializers.CharField()
    isTask = serializers.BooleanField()
    responsible = serializers.CharField(allow_blank=True)
    due = serializers.DateTimeField(allow_null=True)


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
        arrangements_data = [val for val in validated_data['tasks'] if val['isTask'] is False]
        if len(arrangements_data) > 0:
            self.add_arrangements(arrangements_data, new_meeting)
        task_data = [val for val in validated_data['tasks'] if val['isTask'] is True]
        if len(task_data) > 0:
            user =  self.context['request'].user
            self.add_tasks(task_data, new_meeting, user)
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

    @staticmethod
    def add_tasks(data: list, meeting: Meeting, initiator: User) -> None:
        for val in data:
            short_name = val['desc'] if len(val['desc']) <= 20 else val['desc'][:20] + '...'
            create_instance(
                short_name=short_name,
                what_to_do=val['desc'],
                perform_before=val['due'],
                responsible=val['responsible'],
                initiator=initiator,
                meeting=meeting
            )


class GetArrangementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Arrangement
        fields = ['description']


class CmProcessInstanceSerializer(serializers.ModelSerializer):

    responsible = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = CmProcessContext
        fields = ['what_to_do', 'responsible', 'perform_before', 'create_date', 'status']


class GetMeetingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meeting
        fields = ['id', 'name', 'due_of_event', 'description', 'status']


class GetCurrentMeetingsSerializer(serializers.ModelSerializer):

    arrangements = GetArrangementSerializer(many=True, required=False)
    tasks = CmProcessInstanceSerializer(many=True, required=False)

    class Meta:
        model = Meeting
        fields = ['id', 'name', 'due_of_event', 'description', 'status', 'arrangements', 'tasks']


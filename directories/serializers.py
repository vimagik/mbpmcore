from rest_framework import serializers

from directories.models import Meeting


class StartFormMeetingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meeting
        fields = '__all__'

    def create(self, validated_data):
        new_meeting = Meeting.objects.create(**validated_data)
        return new_meeting

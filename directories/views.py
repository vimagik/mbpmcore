from rest_framework import permissions, generics

from directories.serializers import StartFormMeetingSerializer


class CreateMeetingView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StartFormMeetingSerializer

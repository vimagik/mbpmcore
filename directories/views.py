from rest_framework import permissions, generics, viewsets

from directories.serializers import StartFormMeetingSerializer, GetMeetingsSerializer
from directories.models import Meeting


class CreateMeetingView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StartFormMeetingSerializer


class GetMeetingView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GetMeetingsSerializer

    def get_queryset(self):
        query_set = Meeting.objects.all()
        return query_set

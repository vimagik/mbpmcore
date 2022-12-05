from rest_framework import permissions, generics, viewsets
from rest_framework.pagination import PageNumberPagination

from directories.serializers import StartFormMeetingSerializer, GetMeetingsSerializer
from directories.models import Meeting


class CreateMeetingView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StartFormMeetingSerializer


class MeetingPaginator(PageNumberPagination):
    """Pagination for get meetings"""
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100


class GetMeetingView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GetMeetingsSerializer
    pagination_class = MeetingPaginator

    def get_queryset(self):
        query_set = Meeting.objects.all().order_by('due_of_event')
        return query_set

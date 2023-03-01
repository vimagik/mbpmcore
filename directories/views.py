from rest_framework import permissions, generics, viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django.http import Http404

from directories.serializers import StartFormMeetingSerializer, GetMeetingsSerializer, GetCurrentMeetingsSerializer
from directories.models import Meeting


class CreateMeetingView(generics.CreateAPIView):
    """Saving meeting data"""
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]

    def post(self, request) -> Response:
        serializer = StartFormMeetingSerializer(
            data=request.data, 
            context={'request': request}
        )
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


class MeetingPaginator(PageNumberPagination):
    """Pagination for get meetings"""
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100


class GetMeetingView(viewsets.ModelViewSet):
    """Output of all meetings with filtering"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GetMeetingsSerializer
    pagination_class = MeetingPaginator

    def get_queryset(self):
        key_words = self.request.query_params.get('key_words')
        if key_words:
            query_set = Meeting.objects.filter(
                Q(name__icontains=key_words) | Q(description__icontains=key_words)
                )
        else:
            query_set = Meeting.objects.all().order_by('due_of_event')
        start_date = self.request.query_params.get('startDate')
        end_date = self.request.query_params.get('endDate')
        if start_date:
            query_set = query_set.filter(
                Q(due_of_event__gte = start_date) & Q(due_of_event__lte = end_date)
            )
        if self.request.query_params.get('status'):
            meet_status = self.request.query_params.get('status')
            query_set = query_set.filter(status = meet_status)
        if self.request.query_params.get('sort_by[]'):
            sort_by = self.request.query_params.get('sort_by[]')
            sort_desk = self.request.query_params.get('sort_desc[]', default='false')
            if sort_desk == 'true':
                sort_by = '-' + sort_by
            query_set = query_set.order_by(sort_by)
        else:
            query_set = query_set.order_by('-due_of_event')
        return query_set


class GetCurrentMeetView(APIView):
    """Obtaining data about a specific meeting"""
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Meeting.objects.get(pk=pk)
        except Meeting.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        meet = self.get_object(pk)
        meet_serializer = GetCurrentMeetingsSerializer(meet)
        return Response(meet_serializer.data)

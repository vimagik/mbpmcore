from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions, status, viewsets

from core.serializers import TaskSerializer
from core.models import TaskModel


class TasksSetPagination(PageNumberPagination):
    """Pagination для index запроса"""
    page_size = 7
    page_size_query_param = 'page_size'
    max_page_size = 100


class TaskView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TaskSerializer
    pagination_class = TasksSetPagination

    def get_queryset(self):
        queryset_for_responsible = TaskModel.objects.filter(responsible_id__exact=self.request.user.id)
        queryset_for_group = TaskModel.objects.filter(responsible_group__in=self.request.user.groups.all())
        if self.request.query_params.get('search'):
            search_string = self.request.query_params.get('search')
            queryset_for_responsible = queryset_for_responsible.filter(name__istartswith=search_string)
            queryset_for_group = queryset_for_group.filter(name__istartswith=search_string)
        return queryset_for_responsible.union(queryset_for_group)


class UserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = {
            'username': request.user.username,
            'email': request.user.email,
        }
        return Response({'user': data})


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

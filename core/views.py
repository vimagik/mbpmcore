from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status, viewsets

from core.serializers import TaskSerializer
from core.models import TaskModel


class TaskView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = TaskModel.objects.filter(responsible_id__exact=self.request.user.id)
        return queryset


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

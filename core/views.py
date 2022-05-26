from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status


class TaskView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({'Task': [1, 2, 3, 4]})


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

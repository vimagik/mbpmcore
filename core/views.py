from rest_framework.views import APIView
from rest_framework.response import Response


class TaskView(APIView):
    def get(self, request):
        return Response({'Task': [1, 2, 3, 4]})

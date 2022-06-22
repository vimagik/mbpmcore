from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import permissions, status

from conman.serializers import StartFormSerializer


class StartCM(APIView):
    """Start a new process for CM
    camunda -> context -> process instance
    """
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]

    def post(self, request):
        serializer = StartFormSerializer(data=request.data)
        if serializer.is_valid():
            qwe = serializer.data
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

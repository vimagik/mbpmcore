from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import permissions, status

from conman.serializers import StartFormSerializer
from conman.camunda import start_cm


class StartCM(APIView):
    """
    Start a new process for CM
    camunda -> context -> process instance
    """
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]

    def post(self, request):
        serializer = StartFormSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        status_code, camunda_response = start_cm(serializer.data.get('responsible'))
        if not status_code:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=camunda_response)
        process_instance_id = camunda_response.get('id')
        return Response(status=status.HTTP_201_CREATED)

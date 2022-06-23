from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import permissions, status
from datetime import datetime

from conman.serializers import StartFormSerializer
from conman.camunda import start_cm
from conman.models import CmProcessContext
from core.models import ProcessInstanceModel, ProcessModel

PROCESS_CODE = 'cm'

class StartCM(APIView):
    """
    Start a new process for CM
    camunda -> context -> process instance
    """
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]

    def post(self, request):
        """Create new instance"""
        serializer = StartFormSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        status_code, camunda_response = start_cm(serializer.validated_data.get('responsible'))
        if not status_code:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=camunda_response)

        context = serializer.save()
        context.initiator = request.user
        context.camunda_instance_id = camunda_response.get('id')
        context.save()

        process = ProcessModel.objects.get(code__exact=PROCESS_CODE)
        ProcessInstanceModel.objects.create(
            camunda_instance_id=camunda_response.get('id'),
            process=process,
        )
        return Response(status=status.HTTP_201_CREATED)

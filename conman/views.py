from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import permissions, status, viewsets
from rest_framework.pagination import PageNumberPagination

from conman.serializers import StartFormSerializer, ContextSerializer, FinishPlanTaskSerializer, \
    FinishCompleteTaskSerializer, CmProcessInstanceSerializer
from conman.camunda import start_cm
from conman.models import CmProcessContext
from core.models import ProcessInstanceModel, ProcessModel
from core.camunda import complete_task

PROCESS_CODE = 'cm'


class StartCM(APIView):
    """
    Start a new process for CM
    camunda -> context -> process instance
    """
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]

    def post(self, request) -> Response:
        """Create new instance"""
        process_status = 'Планирование'
        serializer = StartFormSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        perform_before = serializer.validated_data['perform_before']
        if perform_before:
            perform_before = perform_before.isoformat()[:19] + '.000UTC'
            process_status = 'Выполнение'

        status_code, camunda_response = start_cm(
            serializer.validated_data['responsible'],
            serializer.validated_data['short_name'],
            perform_before,
        )
        if not status_code:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=camunda_response)

        context = serializer.save()
        context.initiator = request.user
        context.camunda_instance_id = camunda_response.get('id')
        context.status = process_status
        context.save()

        process = ProcessModel.objects.get(code__exact=PROCESS_CODE)
        ProcessInstanceModel.objects.create(
            camunda_instance_id=camunda_response.get('id'),
            process=process,
        )
        return Response(status=status.HTTP_201_CREATED)


class GetContextView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request) -> Response:
        context_id = request.query_params.get('context')
        if not context_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        context_process = CmProcessContext.objects.get(camunda_instance_id__exact=request.query_params.get('context'))
        serializer = ContextSerializer(context_process, many=False)
        return Response(serializer.data)


class FinishPlanTaskView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]

    def get(self, request) -> Response:
        serializer = FinishPlanTaskSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        perform_before = serializer.validated_data['perform_before']
        perform_before_str = perform_before.isoformat()[:19] + '.000UTC'
        task_id = serializer.validated_data['task_id']
        instance_id = serializer.validated_data['instance_id']
        variables = {
            "task_restriction": {"value": perform_before_str, "type": "Date"},
        }
        status_code, camunda_response = complete_task(task_id, variables)
        if not status_code:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=camunda_response)
        process_instance = CmProcessContext.objects.get(camunda_instance_id__exact=instance_id)
        process_instance.perform_before = perform_before
        process_instance.status = 'Выполнение'
        process_instance.save()
        return Response(status=status.HTTP_200_OK)


class FinishCompleteTaskView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]

    def get(self, request) -> Response:
        process_status = 'Завершен'
        serializer = FinishCompleteTaskSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        task_id = serializer.validated_data['task_id']
        instance_id = serializer.validated_data['instance_id']
        status_task = serializer.validated_data['status']
        variables = {
            "status": {"value": status_task, "type": "String"},
        }
        if status_task == 'postponement':
            perform_before = serializer.validated_data['perform_before']
            perform_before_str = perform_before.isoformat()[:19] + '.000UTC'
            variables['task_restriction'] = {"value": perform_before_str, "type": "Date"}
            process_status = 'Перенос срока'
        status_code, camunda_response = complete_task(task_id, variables)
        if not status_code:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=camunda_response)
        process_instance = CmProcessContext.objects.get(camunda_instance_id__exact=instance_id)
        if status_task == 'postponement':
            process_instance.perform_before = perform_before
        process_instance.status = process_status
        process_instance.save()
        return Response(status=status.HTTP_200_OK)


class CmSetPagination(PageNumberPagination):
    """Pagination for CM process instance"""
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100


class CmProcessInstanceView(viewsets.ModelViewSet):
    """CM process instance for index page"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CmProcessInstanceSerializer
    pagination_class = CmSetPagination

    def get_queryset(self):
        queryset_for_initiator = CmProcessContext.objects.filter(initiator_id__exact=self.request.user.id)
        queryset_for_responsible = CmProcessContext.objects.filter(responsible_id__exact=self.request.user.id)
        result_query = queryset_for_initiator.union(queryset_for_responsible)
        if self.request.query_params.get('sort_by[]'):
            sort_by = self.request.query_params.get('sort_by[]')
            if self.request.query_params.get('sort_desc[]'):
                sort_by = '-' + sort_by
            result_query = result_query.order_by(sort_by)
        return result_query

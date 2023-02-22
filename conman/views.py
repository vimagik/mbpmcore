from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import permissions, status, viewsets
from rest_framework.pagination import PageNumberPagination

from conman.serializers import StartFormSerializer, ContextSerializer, FinishPlanTaskSerializer, \
    FinishCompleteTaskSerializer, CmProcessInstanceSerializer
from conman.camunda import create_instance
from conman.models import CmProcessContext
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
        serializer = StartFormSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        status_code, status_text = create_instance(
            short_name=serializer.validated_data['short_name'],
            what_to_do=serializer.validated_data['what_to_do'],
            perform_before=serializer.validated_data['perform_before'],
            responsible=serializer.validated_data['responsible'],
            initiator=request.user
        )
        
        if not status_code:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=status_text)

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
        else:
            if process_instance.meeting:
                all_task = CmProcessContext.objects.filter(
                    meeting__pk=process_instance.meeting.pk
                    ).exclude(
                    pk=process_instance.pk
                    )
                completed = True
                for task in all_task:
                    if task.status != 'Завершен':
                        completed = False
                        break
                if completed:
                    process_instance.meeting.status = 'Все поручения выполнены'
                    process_instance.meeting.save()
        process_instance.status = process_status
        process_instance.save()
        return Response(status=status.HTTP_200_OK)


class CmSetPagination(PageNumberPagination):
    """Pagination for CM process instance"""
    page_size = 100
    max_page_size = 100
    page_size_query_param = 'page_size'


class CmProcessInstanceView(viewsets.ModelViewSet):
    """CM process instance for index page"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CmProcessInstanceSerializer
    pagination_class = CmSetPagination

    def get_queryset(self):
        performer_filter = self.request.query_params.get('performer')
        if performer_filter:
            queryset_for_responsible = CmProcessContext.objects.filter(responsible__username__exact=performer_filter)
            result_query = queryset_for_responsible.filter(initiator_id__exact=self.request.user.id)
        else:
            queryset_for_responsible = CmProcessContext.objects.filter(responsible_id__exact=self.request.user.id)
            queryset_for_initiator = CmProcessContext.objects.filter(initiator_id__exact=self.request.user.id)
        only_active = self.request.query_params.get('only_active', default='false')
        if only_active == 'true':
            if performer_filter:
                result_query = result_query.filter(status__exact='Выполнение')
            else:
                queryset_for_initiator = queryset_for_initiator.filter(status__exact='Выполнение')
                queryset_for_responsible = queryset_for_responsible.filter(status__exact='Выполнение')
        if not performer_filter:
            result_query = queryset_for_initiator.union(queryset_for_responsible)
        if self.request.query_params.get('sort_by[]'):
            sort_by = self.request.query_params.get('sort_by[]')
            sort_desk = self.request.query_params.get('sort_desc[]', default='false')
            if sort_desk == 'true':
                sort_by = '-' + sort_by
            result_query = result_query.order_by(sort_by)
        return result_query

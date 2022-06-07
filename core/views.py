from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions, status, viewsets

from core.serializers import TaskSerializer, ProcesSerializer
from core.models import TaskModel, ProcessModel
from core.camunda import get_all_user_task

DEFAULT_PROCESS_VALUE = {
    'name_ru': 'Процесс не зарегистрирован в системе',
    'name_en': 'Process not registered in the system',
    'code': 'error',
    }


class TasksSetPagination(PageNumberPagination):
    """Pagination for tasks"""
    page_size = 7
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProcessView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProcesSerializer
    queryset = ProcessModel.objects.all()


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

    def post(self):
        try:
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CamundaTaskView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        result, data = get_all_user_task(self.request.user)
        if result:
            page = int(self.request.query_params.get('page', default=1))-1
            search_string = self.request.query_params.get('search')
            if search_string:
                data = [item for item in data if item['name'].lower().startswith(search_string.lower())]
            paginated_tasks = data[page*7:(page+1)*7]
            for task in paginated_tasks:
                process_definition = task['processDefinitionId'].split(':')[0]
                process = ProcessModel.objects.filter(camunda_id__exact=process_definition)
                if process.count() > 0:
                    process_value = {
                        'name_ru': process[0].name_ru,
                        'name_en': process[0].name_en,
                        'code' : process[0].code
                    }
                else:
                    process_value = DEFAULT_PROCESS_VALUE
                task['process'] = process_value
            response_data = {
                'count': len(data),
                'results': paginated_tasks
            }
            return Response(status=status.HTTP_200_OK, data=response_data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data)


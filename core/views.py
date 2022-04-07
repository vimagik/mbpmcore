from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response


def index(request):
    return HttpResponse('Uhu!')


class TaskView(APIView):
    def get(self, request):
        return Response({'Task': [1, 2, 3, 4]})

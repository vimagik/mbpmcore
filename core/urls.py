from django.urls import path

from .views import index, TaskView


urlpatterns = [
    path('', index, name='index'),
    path('apiv1/gettask/', TaskView.as_view(), name='getTask')
]

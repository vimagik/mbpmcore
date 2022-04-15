from django.urls import path
from .views import TaskView

app_name = 'core'

urlpatterns = [
    path('v1/gettask/', TaskView.as_view(), name='getTask'),
]

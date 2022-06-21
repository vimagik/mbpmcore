from django.urls import path
from conman.views import StartCM

app_name = 'conman'

urlpatterns = [
    path('v1/start/', StartCM.as_view(), name='startProcess'),
]

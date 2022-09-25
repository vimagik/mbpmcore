from django.urls import path

from directories.views import CreateMeetingView

app_name = 'meeting'

urlpatterns = [
    path('v1/meetings/', CreateMeetingView.as_view(), name='meeting'),
]

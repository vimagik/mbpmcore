from django.urls import path

from directories.views import CreateMeetingView, GetMeetingView

app_name = 'meeting'

urlpatterns = [
    path('v1/meetings/create/', CreateMeetingView.as_view(), name='meeting'),
    path('v1/meetings/', GetMeetingView.as_view({'get': 'list'}), name='get_meeting'),
]

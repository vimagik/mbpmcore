from django.urls import path
from .views import TaskView, UserView, LogoutView

app_name = 'core'

urlpatterns = [
    path('v1/gettask/', TaskView.as_view(), name='getTask'),
    path('v1/user/', UserView.as_view(), name='getUser'),
    path('v1/logout/', LogoutView.as_view(), name='logout'),
]

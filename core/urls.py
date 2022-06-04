from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import TaskView, UserView, LogoutView, ProcessView, CamundaTaskView

app_name = 'core'

urlpatterns = [
    path('v1/getprocess/', ProcessView.as_view({'get': 'list'}), name='getProcess'),
    path('v1/gettask/', TaskView.as_view({'get': 'list'}), name='getTask'),
    path('v1/user/', UserView.as_view(), name='getUser'),
    path('v1/logout/', LogoutView.as_view(), name='logout'),
    path('v1/getusertask/', CamundaTaskView.as_view(), name='getUserTask'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

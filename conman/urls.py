from django.urls import path
from conman.views import StartCM, GetContextView, FinishPlanTaskView, FinishCompleteTaskView

app_name = 'conman'

urlpatterns = [
    path('v1/start/', StartCM.as_view(), name='startProcess'),
    path('v1/getcontext/', GetContextView.as_view(), name='getContext'),
    path('v1/plantask/complete/', FinishPlanTaskView.as_view(), name='finishPlanTask'),
    path('v1/completetask/complete/', FinishCompleteTaskView.as_view(), name='finishCompleteTask'),
]

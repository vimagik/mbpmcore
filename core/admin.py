from django.contrib import admin

from core.models import ProcessModel, TaskModel, ProcessInstanceModel


@admin.register(ProcessModel)
class ProcessAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'camunda_id')
    list_display_links = ('id', '__str__')


@admin.register(TaskModel)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'process', 'responsible', 'responsible_group')
    list_display_links = ('id', '__str__')


@admin.register(ProcessInstanceModel)
class ProcessInstanceAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__')
    list_display_links = ('id', '__str__')

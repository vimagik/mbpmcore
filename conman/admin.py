from django.contrib import admin

from conman.models import CmProcessContext


@admin.register(CmProcessContext)
class CmProcessContextAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'responsible', 'initiator', 'perform_before')

from django.contrib import admin
from directories.models import Meeting, Arrangement


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'due_of_event')


@admin.register(Arrangement)
class ArrangementAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'create_date')
    readonly_fields = ('create_date',)

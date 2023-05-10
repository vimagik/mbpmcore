from django.contrib import admin
from directories.models import Meeting, Arrangement


class ArrangementInlineAdmin(admin.TabularInline):
    model = Arrangement
    max_num = 5


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'due_of_event')
    inlines = [ArrangementInlineAdmin, ]


@admin.register(Arrangement)
class ArrangementAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'create_date')
    readonly_fields = ('create_date',)

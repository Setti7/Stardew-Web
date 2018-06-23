from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user','contact','version', 'message')
    readonly_fields = [('user', 'contact'), 'version', 'message']
    fields = ['done', 'time']
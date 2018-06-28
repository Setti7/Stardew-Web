from django.contrib import admin
from .models import UserData, Version

# Register your models here.

@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    list_display = ('user','score', 'uploaded_at')
    fields = ['user', 'file', 'score', 'uploaded_at', 'id']
    readonly_fields = ['uploaded_at', 'id']


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('version', 'critical', 'log', 'date')
    fields = [('version', 'critical'), 'log', 'date']
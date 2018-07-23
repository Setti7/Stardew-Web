from django.contrib import admin
from .models import UserData, Version
from django.utils.html import format_html

# Register your models here.

@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'version_link', 'processed', 'score', 'id', 'uploaded_at',)
    fields = ['user', 'file', 'score', 'uploaded_at', 'id']
    readonly_fields = ['uploaded_at', 'id']
    date_hierarchy = 'uploaded_at'
    actions = ['mark_as_processed', 'unmark_as_processed']

    list_filter = ('version', 'processed')

    def version_link(self, obj):
        url = '/admin/Data/version/%s/change/' % obj.version.id
        return format_html("<a href='{}'>{}</a>", url, obj.version)
    version_link.admin_order_field = 'version'
    version_link.short_description = 'version'

    def mark_as_processed(self, request, queryset):
        rows_updated = queryset.update(processed=True)
        if rows_updated == 1:
            message_bit = "1 userdata was"
        else:
            message_bit = "%s userdatas were" % rows_updated
        self.message_user(request, "%s successfully marked as processed." % message_bit)
    mark_as_processed.short_description = "Mark selected userdatas as read"

    def unmark_as_processed(self, request, queryset):
        rows_updated = queryset.update(processed=False)
        if rows_updated == 1:
            message_bit = "1 userdata was"
        else:
            message_bit = "%s userdatas were" % rows_updated
        self.message_user(request, "%s successfully unmarked as processed." % message_bit)
    unmark_as_processed.short_description = "Unmark selected userdatas as read"

@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('version', 'critical', 'log', 'date')
    fields = [('version', 'critical'), 'log', 'date']
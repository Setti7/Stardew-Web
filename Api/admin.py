from django.contrib import admin
from django.utils.html import format_html

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('details', 'read', 'short_message', 'user_link', 'version_link')
    fields = ['read', 'version', 'time', 'user', 'message']
    readonly_fields = ['time', 'user', 'version', 'message']

    actions = ['mark_as_read', 'unmark_as_read']
    date_hierarchy = 'time'
    list_filter = ('read', 'version')

    def version_link(self, obj):
        url = '/admin/Data/version/%s/change/' % obj.version.id
        return format_html("<a href='{}'>{}</a>", url, obj.version)

    version_link.admin_order_field = 'version'
    version_link.short_description = 'version'

    def user_link(self, obj):
        url = f'/admin/auth/user/{obj.user.id}/change/'
        return format_html("<a href='{}'>{}</a>", url, obj.user)

    user_link.admin_order_field = 'user'
    user_link.short_description = 'user'

    def details(self, obj):
        url = '/admin/Api/message/%s/change/' % obj.id
        return format_html("<a href='{}'>More</a>", url)

    details.admin_order_field = 'Details'
    details.short_description = 'Details'

    def mark_as_read(self, request, queryset):
        rows_updated = queryset.update(read=True)
        if rows_updated == 1:
            message_bit = "1 message was"
        else:
            message_bit = "%s messages were" % rows_updated
        self.message_user(request, "%s successfully marked as read." % message_bit)

    mark_as_read.short_description = "Mark selected messages as read"

    def unmark_as_read(self, request, queryset):
        rows_updated = queryset.update(read=False)
        if rows_updated == 1:
            message_bit = "1 message was"
        else:
            message_bit = "%s messages were" % rows_updated
        self.message_user(request, "%s successfully unmarked as read." % message_bit)

    unmark_as_read.short_description = "Unmark selected messages as read"

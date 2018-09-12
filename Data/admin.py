from django.contrib import admin
from django.utils.html import format_html

from .models import UserData, Version, Profile


# Register your models here.

@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    list_display = ('user_link', 'version_link', 'processed', 'score', 'id', 'uploaded_at', 'edit_link')
    fields = ['user', 'file', 'score', 'uploaded_at', 'id']
    readonly_fields = ['uploaded_at', 'id']

    date_hierarchy = 'uploaded_at'
    actions = ['mark_as_processed', 'unmark_as_processed']
    list_filter = ('version', 'processed')

    def edit_link(self, obj):
        url = '/admin/Data/userdata/%s/change/' % obj.id
        return format_html("<strong><a href='{}'>Edit</a></strong>", url)

    edit_link.admin_order_field = 'details'
    edit_link.short_description = 'details'

    def user_link(self, obj):
        url = '/admin/auth/user/%s/change/' % obj.user.id
        return format_html("<a href='{}'>{}</a>", url, obj.user)

    user_link.admin_order_field = 'user'
    user_link.short_description = 'user'

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


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_link', 'score', 'edit_link')
    fields = ['user', 'score']

    actions = ['reset_score']

    def user_link(self, obj):
        url = '/admin/auth/user/%s/change/' % obj.user.id
        return format_html("<strong><a href='{}'>{}</a></strong>", url, obj.user)

    user_link.admin_order_field = 'user'
    user_link.short_description = 'user'

    def edit_link(self, obj):
        url = '/admin/Data/profile/%s/change/' % obj.id
        return format_html("<strong><a href='{}'>Edit</a></strong>", url)

    edit_link.admin_order_field = 'details'
    edit_link.short_description = 'details'

    def reset_score(self, request, queryset):
        rows_updated = queryset.update(score=0)
        if rows_updated == 1:
            message_bit = "1 profile was"
        else:
            message_bit = "%s profiles were" % rows_updated
        self.message_user(request, "%s successfully reset." % message_bit)

    reset_score.short_description = "Reset profile score"

from django import template
from django.contrib.auth.models import Group, User

register = template.Library()


@register.filter(name='has_group')
def has_group(username, group_name):
    try:
        user = User.objects.get(username=username)

        if group_name == 'staff':
            return user.is_staff

        group = Group.objects.get(name=group_name)
        return group in user.groups.all()

    except:
        return None

from django import template
from django.contrib.auth.models import Group, User

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    try:
        username = User.objects.get(username=user)
        group =  Group.objects.get(name=group_name)
        return group in username.groups.all()

    except:
        return None
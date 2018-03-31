from django.db import models
from django.contrib.auth.models import User
# import numpy as np


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'userdata/{0}/{1}'.format(instance.user, filename)


class UserData(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    file = models.FileField(upload_to=user_directory_path)
    score = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
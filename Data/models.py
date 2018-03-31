from django.db import models
# import numpy as np


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'userdata/{0}/{1}'.format(instance.username, filename)


class UserData(models.Model):
    user = models.CharField(max_length=40)
    file = models.FileField(upload_to=user_directory_path)
    score = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

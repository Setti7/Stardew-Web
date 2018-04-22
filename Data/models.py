from django.db import models
from django.contrib.auth.models import User
# import numpy as np


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'userdata/{0}/{1}'.format(instance.user, filename)


class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path)
    score = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-score"]
        verbose_name_plural = 'User Data'

    def __str__(self):
        return "{}".format(str(self.user))

class Version(models.Model):
    version = models.CharField(max_length=20, unique=True)
    log = models.TextField(max_length=200)
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['date']
        verbose_name = "Version"
        verbose_name_plural = "Version"

    def as_dict(self):
        return {
            "Version": self.version,
            "Changes": self.log,
            "Date": self.date
        }

    def __str__(self):
        return "{}".format(str(self.version))
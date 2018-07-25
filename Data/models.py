from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
# import numpy as np


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'userdata/{0}/{1}.npy'.format(instance.user, instance.id)


class UserData(models.Model):
    id =  models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path)
    score = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField()
    version = models.ForeignKey('Version', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ["-score"]
        verbose_name_plural = 'User Data'

    def __str__(self):
        return "{}".format(str(self.user))

class Version(models.Model):
    version = models.CharField(max_length=20, unique=True)
    log = models.TextField(max_length=500)
    date = models.DateField()
    critical = models.BooleanField()

    class Meta:
        ordering = ['-date']
        verbose_name = "Version"
        verbose_name_plural = "Version"

    def as_dict(self):
        return {
            "Version": self.version,
            "Changes": self.log,
            "Date": self.date,
            "Critical": self.critical
        }

    def __str__(self):
        return "{}".format(str(self.version))

# class Message(models.Model): # Make it accept bigger messages, but cut them when 240 is exceded
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     message = models.TextField(max_length=240)
#     time = models.DateTimeField()
#
#     class Meta:
#          ordering = ['-time']
#
#     def as_dict(self):
#         return {
#             "User": self.user,
#             "Time": self.time,
#             "Message": self.message
#         }
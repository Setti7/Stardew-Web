from django.db import models
from Data.models import Version
from django.contrib.auth.models import User


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    message = models.TextField(max_length=1000)
    contact = models.EmailField(null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)
    version = models.ForeignKey(Version, on_delete=models.SET_NULL, null=True)
    read = models.BooleanField()

    class Meta:
         ordering = ['-time']

    def as_dict(self):
        return {
            "User": self.user,
            "Time": self.time,
            "Message": self.message,
            "Contact": self.contact,
            "Version": self.version,
            "Read": self.read
        }
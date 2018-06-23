from django.db import models
from django.contrib.auth.models import User


class Message(models.Model): # Make it accept bigger messages, but cut them when 240 is exceded
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    message = models.TextField(max_length=240)
    contact = models.EmailField(null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)
    version = models.CharField(max_length=10)
    done = models.BooleanField(default=False)

    class Meta:
         ordering = ['-time']

    def as_dict(self):
        return {
            "User": self.user,
            "Time": self.time,
            "Message": self.message,
            "Contact": self.contact,
            "Version": self.version,
            "Done": self.done
        }
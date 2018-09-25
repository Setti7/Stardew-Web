from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import truncatechars # truncatewords
from rest_framework.authtoken.models import Token

from Data.models import Version


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    message = models.TextField(max_length=1000)
    time = models.DateTimeField(auto_now_add=True)
    version = models.ForeignKey(Version, on_delete=models.SET_NULL, null=True)
    read = models.BooleanField()

    class Meta:
        ordering = ['-time']

    @property
    def short_message(self):
        return truncatechars(self.message, 75)

    def as_dict(self):
        return {
            "User": self.user,
            "Time": self.time,
            "Message": self.message,
            "Version": self.version,
            "Read": self.read
        }


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

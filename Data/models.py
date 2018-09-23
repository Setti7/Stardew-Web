import os
from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum

from django.db.models.signals import post_save
from django.dispatch import receiver


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'userdata/{0}/{1}.npy'.format(instance.user, instance.id)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    class Meta:
        ordering = ["-user"]
        verbose_name_plural = 'Profile'

    def __str__(self):
        return f"Profile of {str(self.user)}"


class UserData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path)
    score = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField()
    version = models.ForeignKey('Version', on_delete=models.SET_NULL, null=True)

    # TODO: if fishing session was successful: successful = models.BooleanField()

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


@receiver(post_save, sender=UserData)
def update_user_score(sender, instance, **kwargs):
    profile = Profile.objects.get(user=instance.user)
    profile.score += instance.score
    profile.save()


@receiver(models.signals.post_delete, sender=UserData)
def delete_file(sender, instance, *args, **kwargs):
    """ Deletes files on `post_delete` """
    if instance.file:

        if os.path.isfile(instance.file.path):
            profile = Profile.objects.get(user=instance.user)
            profile.score -= instance.score

            # If profile score is negative for some reason, sum every user_data sent from this user to get real score
            if profile.score < 0:
                profile.score = UserData.objects.filter(user=instance.user).aggregate(Sum('score'))['score__sum']

            os.remove(instance.file.path)
            profile.save()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

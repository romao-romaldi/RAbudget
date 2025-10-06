from django.db import models
from django.contrib.auth.models import User as Users
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    bio = models.CharField(max_length=100, null=True, blank=True)
    pid = models.UUIDField(auto_created=True, default=uuid.uuid4, unique=True, editable=False)

    last_name = models.CharField(max_length=100, default="", blank=True , null=True)
    first_name = models.CharField(max_length=100, default="", blank=True , null=True)
    tel = models.CharField(max_length=25)
    tel2 = models.CharField(max_length=100, default="", blank=True , null=True)
    pays = models.CharField(max_length=100, default="", blank=True , null=True)
    ville = models.CharField(max_length=100, default="", blank=True , null=True)
    addresse = models.CharField(max_length=100, default="", blank=True , null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


def create_user_profile(sender, instance, created, **kwargs):
    if created:

        pid = uuid.uuid4()
        while len(Profile.objects.filter(pid=pid)) > 0:
            pid = uuid.uuid4()

        Profile.objects.create(user=instance, pid=pid)


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile, sender=Users)
post_save.connect(save_user_profile, sender=Users)


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


# Modèle pour gérer les logos du site
class Logo(models.Model):
    """
    Modèle pour gérer les logos affichés dans la navbar
    Permet de télécharger et gérer différents logos pour le site
    """
    nom = models.CharField(max_length=100, help_text="Nom du logo (ex: Logo principal)")
    image = models.ImageField(
        upload_to='logos/',
        help_text="Image du logo (formats: PNG, JPG, SVG)"
    )
    est_actif = models.BooleanField(
        default=False,
        help_text="Logo actuellement utilisé dans la navbar"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Description optionnelle du logo"
    )
    date_upload = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Logo"
        verbose_name_plural = "Logos"
        ordering = ['-date_modification']

    def __str__(self):
        return f"{self.nom} ({'Actif' if self.est_actif else 'Inactif'})"

    def save(self, *args, **kwargs):
        # Si ce logo devient actif, désactiver tous les autres
        if self.est_actif:
            Logo.objects.filter(est_actif=True).exclude(pk=self.pk).update(est_actif=False)
        super().save(*args, **kwargs)

    @classmethod
    def get_logo_actif(cls):
        """Retourne le logo actuellement actif"""
        return cls.objects.filter(est_actif=True).first()


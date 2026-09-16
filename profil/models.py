from django.db import models
from django.conf import settings

class Profil(models.Model):

    utilisateur = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profil'
    )

    telephone = models.CharField(max_length=30, blank=True)

    whatsapp = models.CharField(max_length=30, blank=True)

    adresse = models.CharField(max_length=255, blank=True)

    ville = models.CharField(max_length=100, blank=True)

    photo = models.ImageField(
        upload_to='profils/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.utilisateur.username

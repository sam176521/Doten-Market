from django.db import models
from django.conf import settings


class Notification(models.Model):

    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    titre = models.CharField(
        max_length=200
    )

    message = models.TextField()

    lu = models.BooleanField(
        default=True
    )

    date_creation = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.titre
# Create your models here.

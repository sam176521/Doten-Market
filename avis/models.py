from django.db import models
from django.contrib.auth.models import User
from produits.models import Produit
from django.conf import settings
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator



class Avis(models.Model):

    produit = models.ForeignKey(
        Produit,
        on_delete=models.CASCADE,
        related_name='avis_produit'
    )

    utilisateur = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE
    )

    note = models.IntegerField(
    validators=[
        MinValueValidator(1),
        MaxValueValidator(5)
    ]
    )

    commentaire = models.TextField()

    date_creation = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.utilisateur} - {self.produit}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['produit', 'utilisateur'],
                name='avis_produit_unique_par_utilisateur'
            )
        ]

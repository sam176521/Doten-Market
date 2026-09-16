from django.db import models
from django.conf import settings
from produits.models import Produit


class Panier(models.Model):

    client = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    date_creation = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Panier de {self.client.username}"


class LignePanier(models.Model):

    panier = models.ForeignKey(
        Panier,
        on_delete=models.CASCADE,
        related_name='lignes'
    )

    produit = models.ForeignKey(
        Produit,
        on_delete=models.CASCADE
    )

    quantite = models.PositiveIntegerField(default=1)

    def sous_total(self):
        return self.quantite * self.produit.prix

    def __str__(self):
        return f"{self.produit.nom} x {self.quantite}"

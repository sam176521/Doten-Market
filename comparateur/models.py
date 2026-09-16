from django.db import models
from produits.models import Produit
from boutiques.models import Boutique


class Comparaison(models.Model):

    produit = models.ForeignKey(
        Produit,
        on_delete=models.CASCADE
    )

    boutique = models.ForeignKey(
        Boutique,
        on_delete=models.CASCADE
    )

    prix = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return self.produit.nom


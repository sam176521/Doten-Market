from django.db import models
from django.conf import settings
from produits.models import Produit

class Panier(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    prduit = models.ForeignKey(Produit,on_delete=models.CASCADE)
    quantite = models.IntegerField(default=1)

    def total(self):
        return self.produit.prix * self.quantite

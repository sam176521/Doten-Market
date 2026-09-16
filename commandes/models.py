from django.db import models
from django.conf import settings
from produits.models import Produit


class Commande(models.Model):

    STATUTS = (
        ('attente', 'En attente'),
        ('confirmee', 'Confirmée'),
        ('preparee', 'Préparée'),
        ('livree', 'Livrée'),
        ('annulee', 'Annulée'),
    )

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='commandes'
    )

    montant_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    statut = models.CharField(
        max_length=20,
        choices=STATUTS,
        default='attente'
    )

    date_commande = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Commande #{self.id}"


class LigneCommande(models.Model):

    commande = models.ForeignKey(
        Commande,
        on_delete=models.CASCADE,
        related_name='lignes'
    )

    produit = models.ForeignKey(
        Produit,
        on_delete=models.CASCADE
    )

    quantite = models.PositiveIntegerField()

    prix_unitaire = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    sous_total = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.produit.nom} x {self.quantite}"

class HistoriqueVente(models.Model):

    boutique = models.ForeignKey(
        'boutiques.Boutique',
        on_delete=models.CASCADE,
        related_name='historique_ventes'
    )

    produit = models.ForeignKey(
        'produits.Produit',
        on_delete=models.CASCADE
    )

    commande = models.ForeignKey(
        Commande,
        on_delete=models.CASCADE,
        related_name='historique_ventes'
    )

    quantite = models.PositiveIntegerField()

    prix_unitaire = models.DecimalField(
        max_digits=12,
        decimal_places = 2
    )

    date_vente = models.DateTimeField(
        auto_now_add=True
    )

    montant_total = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    paiement = models.ForeignKey(
        'paiements.Paiement',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.produit.nom}"

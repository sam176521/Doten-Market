from django.db import models
from commandes.models import Commande


class Paiement(models.Model):

    METHODES = (
        ('orange', 'Orange Money'),
        ('airtel', 'Airtel Money'),
        ('mpesa', 'M-Pesa'),
    )

    STATUTS = (
        ('attente', 'En attente'),
        ('valide', 'Validé'),
        ('echec', 'Échec'),
    )

    commande = models.OneToOneField(
        Commande,
        on_delete=models.CASCADE
    )

    methode = models.CharField(
        max_length=20,
        choices=METHODES
    )

    montant = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    reference = models.CharField(
        max_length=100,
        unique=True
    )

    statut = models.CharField(
        max_length=20,
        choices=STATUTS,
        default='attente'
    )

    date_paiement = models.DateTimeField(
        auto_now_add=True
    )

    
    numero_telephone = models.CharField(
        max_length=30,
        blank=True
    )

    reference_transaction = models.CharField(
        max_length=120,
        blank=True
    )

    def __str__(self):
        return f"Paiement {self.reference}"

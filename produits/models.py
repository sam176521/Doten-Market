from django.db import models
from boutiques.models import Boutique
from django.db.models import Avg
from django.core.validators import MinValueValidator
class Categorie(models.Model):

    nom = models.CharField(max_length=120)

    image = models.ImageField(
        upload_to='categories/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.nom
    
class Produit(models.Model):
    ETAT_CHOICES = (
        ('neuf', 'Neuf'),
        ('comme_neuf', 'Comme neuf'),
        ('occasion', 'Occasion'),
        ('reconditionne', 'Reconditionne'),
    )

    boutique = models.ForeignKey(Boutique, on_delete=models.CASCADE)
    nom = models.CharField(max_length=120)
    description = models.TextField()
    marque = models.CharField(max_length=120, blank=True)
    qualite = models.CharField(max_length=120, blank=True)
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES, default='neuf')
    origine = models.CharField(max_length=120, blank=True)
    garantie = models.CharField(max_length=120, blank=True)
    details_credibilite = models.TextField(blank=True)
    prix = models.DecimalField(max_digits=10,decimal_places=2, validators=[MinValueValidator(0)])
    image = models.ImageField(
    upload_to='produits/',
    blank=True,
    null=True
)
    stock = models.PositiveIntegerField(default=1)
    categorie = models.ForeignKey(
    Categorie,
    on_delete=models.SET_NULL,
    null=True,
    blank=True
)

    def __str__(self):
            return self.nom



    @property
    def note_moyenne(self):

        return self.avis_produit.aggregate(
            Avg('note')
        )['note__avg'] or 0

    @property
    def score_credibilite(self):
        champs = [
            self.description,
            self.marque,
            self.qualite,
            self.origine,
            self.garantie,
            self.details_credibilite,
        ]
        return sum(1 for champ in champs if champ) * 100 // len(champs)


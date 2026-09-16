from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg

class Boutique(models.Model):
    proprietaire = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nom = models.CharField(max_length=120)
    description = models.TextField()
    logo = models.ImageField(
    upload_to='boutiques/',
    blank=True,
    null=True
)
    note = models.FloatField(default=0)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom

    @property
    def note_moyenne(self):
        return self.avis_boutique.aggregate(moyenne=Avg('note'))['moyenne'] or 0

    @property
    def nombre_avis(self):
        return self.avis_boutique.count()



class AvisBoutique(models.Model):

    NOTE_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    boutique = models.ForeignKey(
        Boutique,
        on_delete=models.CASCADE,
        related_name='avis_boutique'
    )

    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    note = models.IntegerField(
        choices=NOTE_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    commentaire = models.TextField()

    date_creation = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.boutique.nom} - {self.note}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['boutique', 'utilisateur'],
                name='avis_boutique_unique_par_utilisateur'
            )
        ]

from django import forms
from .models import Produit


class ProduitForm(forms.ModelForm):

    class Meta:

        model = Produit

        fields = [
            'nom',
            'description',
            'marque',
            'qualite',
            'etat',
            'origine',
            'garantie',
            'details_credibilite',
            'prix',
            'stock',
            'categorie',
            'image',
        ]

        labels = {
            'qualite': 'Qualite / finition',
            'details_credibilite': 'Details de credibilite',
            'origine': 'Origine du produit',
            'garantie': 'Garantie ou condition SAV',
        }

        help_texts = {
            'details_credibilite': "Matiere, dimensions, contenu de la boite, preuve d'authenticite, delai de livraison...",
        }

import re
import unicodedata
from difflib import SequenceMatcher

from .models import Produit


def normaliser_nom_produit(nom):
    valeur = unicodedata.normalize('NFKD', nom or '').encode('ascii', 'ignore').decode('ascii')
    valeur = re.sub(r'[^a-zA-Z0-9\s]', ' ', valeur).lower()
    mots_vides = {'de', 'du', 'des', 'le', 'la', 'les', 'un', 'une', 'et', 'the'}
    mots = [mot for mot in valeur.split() if mot not in mots_vides]
    return ' '.join(mots)


def score_similarite_produit(nom_a, nom_b):
    a = normaliser_nom_produit(nom_a)
    b = normaliser_nom_produit(nom_b)

    if not a or not b:
        return 0

    mots_a = set(a.split())
    mots_b = set(b.split())
    intersection = len(mots_a & mots_b)
    union = len(mots_a | mots_b) or 1
    score_mots = intersection / union
    score_sequence = SequenceMatcher(None, a, b).ratio()
    return round(max(score_mots, score_sequence) * 100)


def produits_similaires(produit, seuil=72):
    produits = []
    candidats = Produit.objects.select_related('boutique', 'categorie').exclude(pk=produit.pk)

    for candidat in candidats:
        score = score_similarite_produit(produit.nom, candidat.nom)
        if score >= seuil:
            candidat.score_comparaison = score
            produits.append(candidat)

    return sorted(produits, key=lambda item: (item.prix, -item.score_comparaison))

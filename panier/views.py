from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render

from produits.models import Produit
from .models import Panier
from .models import LignePanier

from django.contrib import messages

def ajouter_panier(request, produit_id):

    if not request.user.is_authenticated:
        return redirect('login')

    produit = get_object_or_404(
        Produit,
        id=produit_id
    )

    panier, created = Panier.objects.get_or_create(
        client=request.user
    )

    ligne, created = LignePanier.objects.get_or_create(
        panier=panier,
        produit=produit
    )

    if not created:
        ligne.quantite += 1
        ligne.save()

    

    messages.success(
        request,
        "Produit ajouté au panier."
    )

    return redirect(
        request.META.get(
            'HTTP_REFERER',
            '/'
        )
    )

def voir_panier(request):

    panier, created = Panier.objects.get_or_create(
        client = request.user
    )


    total = sum(
        ligne.sous_total()
        for ligne in panier.lignes.all()
    )

    return render(
        request,
        'panier/voir_panier.html',
        {
            'panier':panier,
            'total':total
        ,
        'breadcrumb': [
            ('Accueil', '/'),
            ('Panier', None),
        ]
      }          
    )




def supprimer_ligne(request, ligne_id):

    ligne = get_object_or_404(
        LignePanier,
        id=ligne_id
    )

    if ligne.panier.client != request.user:
        return redirect('/')

    ligne.delete()

    return redirect(
        'voir_panier'
    )

def augmenter_quantite(request, ligne_id):

    ligne = get_object_or_404(
        LignePanier,
        id=ligne_id
    )

    if ligne.panier.client != request.user:
        return redirect('/')

    ligne.quantite += 1

    ligne.save()

    return redirect(
        'voir_panier'
    )

def diminuer_quantite(request, ligne_id):
    
    ligne = get_object_or_404(
        LignePanier,
        id=ligne_id
    )
    
    if ligne.panier.client != request.user:
        return redirect('/')

    if ligne.quantite > 1:

        ligne.quantite -= 1

        ligne.save()

    else:

        ligne.delete()

    return redirect(
        'voir_panier'
    )
# Create your views here.

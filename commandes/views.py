from decimal import Decimal

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from panier.models import Panier
from commandes.models import Commande, LigneCommande
from .models import HistoriqueVente

from notifications.models import Notification
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Commande
from boutiques.models import Boutique


@login_required
def passer_commande(request):

    panier = Panier.objects.get(
        client=request.user
    )

    lignes_panier = panier.lignes.all()

    if not lignes_panier.exists():
        return redirect('voir_panier')

    commande = Commande.objects.create(
        client=request.user
    )

    total = Decimal('0.00')

    for ligne in lignes_panier:

        sous_total = ligne.quantite * ligne.produit.prix

        LigneCommande.objects.create(
            commande=commande,
            produit=ligne.produit,
            quantite=ligne.quantite,
            prix_unitaire=ligne.produit.prix,
            sous_total=sous_total
        )

        HistoriqueVente.objects.create(
            boutique=ligne.produit.boutique,
            produit=ligne.produit,
            commande=commande,
            quantite=ligne.quantite,
            prix_unitaire=ligne.produit.prix,
            montant_total=sous_total
        )

        total += sous_total

        ligne.produit.stock -= ligne.quantite

        if ligne.produit.stock < ligne.quantite:
             messages.error(
                request,
                "Stock insuffisant ! Nous réaprovisionerons les stocks bientôt."
            )
             
             return redirect('voir_panier')
        else:
            ligne.produit.save()

            Notification.objects.create(
                utilisateur=request.user,
                titre="Commande enregistrée",
                message=f"Votre commande #{commande.id} a été créée."
            )

    commande.montant_total = total
    commande.save()

    lignes_panier.delete()

    
    

    return redirect('mes_commandes') 





def detail_commande(request, commande_id):

    commande = get_object_or_404(
        Commande,
        id=commande_id
    )

    return render(
        request,
        'commandes/detail_commande.html',
        {
            'commande': commande,
        'breadcrumb': [
            ('Accueil', '/'),
            ('Mes commandes', '/commandes/mes-commandes/'),
            (f'Commande #{commande.id}', None),
        ]
        }
    )




@login_required
def mes_commandes(request):

    commandes = Commande.objects.filter(
        client=request.user
    ).order_by(
        '-date_commande'
    )

    return render(
        request,
        'commandes/mes_commandes.html',
        {
            'commandes': commandes,
        'breadcrumb': [
            ('Accueil', '/'),
            ('Mes commandes', None),
        ]
    }
    )



@login_required
def commandes_boutique(request):

    if request.user.type_user != "vendeur":
        return redirect('/')

    boutique = Boutique.objects.filter(
        proprietaire=request.user
    ).first()

    commandes = Commande.objects.filter(
        lignes__produit__boutique=boutique
    ).distinct().order_by(
        '-date_commande'
    )

    return render(
        request,
        'commandes/commandes_boutique.html',
        {
            'commandes': commandes,
            'boutique': boutique
        }
    )


@login_required
def detail_commande_vendeur(
    request,
    commande_id
):

    commande = get_object_or_404(
        Commande,
        id=commande_id
    )

    return render(
        request,
        'commandes/detail_commande_vendeur.html',
        {
            'commande': commande,
            'breadcrumb': [
                ('Accueil', '/'),
                ('Dashboard', '/dashboard/'),
                ('Commandes', '/commandes/vendeur/'),
                (f'Commande #{commande.id}', None),
            ]
        }
    )

@login_required
def modifier_statut_commande(
    request,
    commande_id,
    statut
):

    commande = get_object_or_404(
        Commande,
        id=commande_id
    )

    commande.statut = statut

    commande.save()

    Notification.objects.create(
        utilisateur=commande.client,
        titre="Commande mise à jour",
        message=f"Votre commande #{commande.id} est maintenant {commande.get_statut_display()}."
    )
   # messages.success(
    #    request,
     #   "Statut modifier avec succès ."
    #)


    return redirect(
        'detail_commande_vendeur',
        commande.id
    )

from django.shortcuts import render, redirect, get_object_or_404
from commandes.models import Commande
from .models import Paiement
import uuid


def payer_commande(request, commande_id):

    commande = get_object_or_404(
        Commande,
        id=commande_id
    )

    # Empêcher un deuxième paiement pour la même commande
    if Paiement.objects.filter(
        commande=commande
    ).exists():

        return redirect(
            'detail_commande',
            commande.id
        )

    if request.method == 'POST':

        methode = request.POST.get(
            'methode'
        )

        numero = request.POST.get(
            'numero_telephone'
        )

        reference_transaction = request.POST.get(
            'reference_transaction'
        )

        reference = str(
            uuid.uuid4()
        )[:12]

        Paiement.objects.create(

            commande=commande,

            methode=methode,

            montant=commande.montant_total,

            reference=reference,

            numero_telephone=numero,

            reference_transaction=reference_transaction,

            statut='valide'

        )

        commande.statut = 'confirmee'
        commande.save()

        return redirect(
            'detail_commande',
            commande.id
        )

    return render(
        request,
        'paiements/payer.html',
        {
            'commande': commande
        }
    )

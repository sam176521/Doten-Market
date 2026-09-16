from .models import Panier


def panier_count(request):

    total = 0

    if request.user.is_authenticated:

        panier = Panier.objects.filter(
            client=request.user
        ).first()

        if panier:

            total = sum(
                ligne.quantite
                for ligne in panier.lignes.all()
            )

    return {
        'panier_count': total
    }

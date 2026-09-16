from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required

from produits.models import Produit
from .models import Avis
from .forms import AvisForm


@login_required
def ajouter_avis(request, pk):

    produit = get_object_or_404(
        Produit,
        id=pk
    )
    existe = Avis.objects.filter(
        produit=produit,
        utilisateur=request.user
    ).exists()

    if existe:
        return redirect(f'/produits/{pk}/')

    if request.method == 'POST':

        form = AvisForm(request.POST)

        if form.is_valid():

            avis = form.save(commit=False)

            avis.produit = produit

            avis.utilisateur = request.user

            avis.save()

            return redirect(
                'detail_produit',
                pk=produit.id
            )

    else:

        form = AvisForm()

    return render(
        request,
        'avis/ajouter.html',
        {
            'form': form,
            'produit': produit
        }
    )

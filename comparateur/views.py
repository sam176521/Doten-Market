from django.shortcuts import render
from produits.models import Produit
from produits.utils import score_similarite_produit

def comparateur(request):
    query = request.GET.get('q', '').strip()
    produits = Produit.objects.select_related('boutique', 'categorie').all().order_by('-id')

    if query:
        produits = produits.filter(nom__icontains=query)

    produits = list(produits)
    groupes = []
    utilises = set()

    for produit in produits:
        if produit.id in utilises:
            continue

        groupe = [produit]
        utilises.add(produit.id)

        for autre in produits:
            if autre.id in utilises:
                continue
            if score_similarite_produit(produit.nom, autre.nom) >= 72:
                groupe.append(autre)
                utilises.add(autre.id)

        groupes.append(sorted(groupe, key=lambda item: item.prix))

    return render(request, 'comparateur/index.html',{
        'produits': produits,
        'groupes': groupes,
        'query' : query,
        'breadcrumb': [
            ('Accueil', '/'),
            ('Comparateur', None),
        ],
    })
# Create your views here.

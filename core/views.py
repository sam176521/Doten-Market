from django.shortcuts import render

from produits.models import Produit
from boutiques.models import Boutique

from produits.models import Categorie

def home(request):

    produits = Produit.objects.all().order_by('-id')[:24]

    boutiques = Boutique.objects.all().order_by('-id')[:8]
    categories = Categorie.objects.all()
    context = {
        'produits': produits,
        'boutiques': boutiques,
        'categories': categories,
    }

    return render(request, 'core/home.html', context)

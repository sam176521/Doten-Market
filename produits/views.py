from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from boutiques.models import Boutique

from .forms import ProduitForm
from .models import Categorie, Produit
from .utils import produits_similaires
from django.db.models import Q
from django.core.paginator import Paginator
from notifications.models import Notification


def liste_produits(request):
    produits = Produit.objects.select_related('boutique', 'categorie').all().order_by('-id')

    query = request.GET.get('q')

    produits = Produit.objects.all().order_by('-id')

    if query:

        produits = produits.filter(

            Q(nom__icontains=query) |

            Q(marque__icontains=query) |

            Q(categorie__nom__icontains=query) |

            Q(boutique__nom__icontains=query)

        ).distinct()

    paginator = Paginator(
        produits,
        24
    )

    page_number = request.GET.get(
        'page'
    )

    produits = paginator.get_page(
        page_number
    )

    return render(request, 'produits/liste.html', {
        'produits': produits,
        'breadcrumb': [
            ('Accueil', '/'),
            ('Produits', None),
        ],

        })



def detail_produit(request, pk):
    produit = get_object_or_404(
        Produit.objects.select_related('boutique', 'categorie', 'boutique__proprietaire'),
        id=pk,
    )
    comparaisons = produits_similaires(produit)
    avis = produit.avis_produit.select_related('utilisateur').all()

    return render(request, 'produits/detail.html', {
        'produit': produit,
        'comparaisons': comparaisons,
        'avis': avis,

        'breadcrumb': [
            ('Accueil', '/'),
            ('Produits', '/produits/'),
            (produit.nom, None),
        ]
    })


@login_required
def ajouter_produit(request):
    if request.user.type_user != "vendeur":
        return redirect('/')

    boutique = Boutique.objects.filter(proprietaire=request.user).first()

    if not boutique:
        return redirect('/boutiques/creer/')

    if request.method == "POST":
        form = ProduitForm(request.POST, request.FILES)

        if form.is_valid():
            produit = form.save(commit=False)
            produit.boutique = boutique
            produit.save()
            return redirect('/dashboard/')
    else:
        form = ProduitForm()

    

    return render(request, 'produits/ajouter.html', {'form': form})


def rechercher_produits(request):
    query = request.GET.get('q', '').strip()
    produits = Produit.objects.none()

    if query:
        produits = Produit.objects.select_related('boutique', 'categorie').filter(nom__icontains=query)

    return render(request, 'produits/recherche.html', {
        'produits': produits,
        'query': query,
    })


def produits_par_categorie(request, pk):
    categorie = get_object_or_404(Categorie, id=pk)
    produits = Produit.objects.select_related('boutique', 'categorie').filter(categorie=categorie)

    return render(request, 'produits/categorie.html', {
        'categorie': categorie,
        'produits': produits,
    })


@login_required
def modifier_produit(request, pk):
    produit = get_object_or_404(Produit, id=pk)

    if produit.boutique.proprietaire != request.user:
        return redirect('/')

    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES, instance=produit)

        if form.is_valid():
            form.save()
            return redirect('/dashboard/')
    else:
        form = ProduitForm(instance=produit)

    return render(request, 'produits/modifier.html', {
        'form': form,
        'produit': produit,
    })


@login_required
def supprimer_produit(request, pk):
    produit = get_object_or_404(Produit, id=pk)

    if produit.boutique.proprietaire != request.user:
        return redirect('/')

    if request.method == 'POST':
        produit.delete()
        return redirect('/dashboard/')

    return render(request, 'produits/supprimer.html', {'produit': produit})

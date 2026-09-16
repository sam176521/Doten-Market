from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from boutiques.models import Boutique

from .forms import ProduitForm
from .models import Categorie, Produit
from .utils import produits_similaires
from django.db.models import Q
from django.core.paginator import Paginator
from notifications.models import Notification
from decimal import Decimal, InvalidOperation
from urllib.parse import urlencode


def liste_produits(request):
    produits = Produit.objects.select_related('boutique', 'categorie').all()
    query = request.GET.get('q', '').strip()
    categorie_id = request.GET.get('categorie', '').strip()
    etat = request.GET.get('etat', '').strip()
    prix_min = request.GET.get('prix_min', '').strip()
    prix_max = request.GET.get('prix_max', '').strip()
    tri = request.GET.get('tri', '-id').strip()

    if query:
        produits = produits.filter(
            Q(nom__icontains=query) |
            Q(description__icontains=query) |
            Q(marque__icontains=query) |
            Q(categorie__nom__icontains=query) |
            Q(categorie__nom__icontains=query) |
            Q(boutique__nom__icontains=query)
        ).distinct()

    if categorie_id.isdigit():
        produits = produits.filter(categorie_id=int(categorie_id))
    if etat in dict(Produit.ETAT_CHOICES):
        produits = produits.filter(etat=etat)

    try:
        if prix_min:
            produits = produits.filter(prix__gte=Decimal(prix_min))
        if prix_max:
            produits = produits.filter(prix__lte=Decimal(prix_max))
    except InvalidOperation:
        prix_min = ''
        prix_max = ''

    tri = {
        '-id': '-id',
        'prix': 'prix',
        '-prix': '-prix',
        'nom': 'nom',
    }.get(tri, '-id')
    produits = produits.order_by(tri)

    filtres = request.GET.copy()
    filtres.pop('page', None)
    filter_query = urlencode(filtres, doseq=True)

    paginator = Paginator(produits, 24)
    produits = paginator.get_page(request.GET.get('page'))

    return render(request, 'produits/liste.html', {
        'produits': produits,
        'categories': Categorie.objects.all().order_by('nom'),
        'etats': Produit.ETAT_CHOICES,
        'query': query,
        'categorie_id': categorie_id,
        'etat': etat,
        'prix_min': prix_min,
        'prix_max': prix_max,
        'tri': tri,
        'filter_query': filter_query,
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
    """Compatibilite avec l'ancienne URL de recherche.

    La recherche principale et ses filtres sont désormais centralisés dans
    la vue de la liste des produits.
    """
    query = request.GET.get('q', '').strip()
    params = urlencode({'q': query}) if query else ''
    destination = reverse('liste_produits')
    return redirect(f'{destination}?{params}' if params else destination)


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

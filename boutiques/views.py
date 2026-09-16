from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render

from profil.models import Profil

from .forms import AvisBoutiqueForm, BoutiqueForm
from .models import AvisBoutique, Boutique

from django.db.models import Q
from django.core.paginator import Paginator

def liste_boutiques(request):
    boutiques = Boutique.objects.prefetch_related('avis_boutique').all().order_by('-id')

    query = request.GET.get('q')

    boutiques = Boutique.objects.all().order_by('-id')
    if query:

        boutiques = boutiques.filter(

            Q(nom__icontains=query) |

            Q(note__icontains=query) |

            Q(date_creation__icontains=query) |

            Q(proprietaire__icontains=query)

        ).distinct()

    paginator = Paginator(
        boutiques,
        12
    )

    page_number = request.GET.get(
        'page'
    )

    boutiques = paginator.get_page(
        page_number
    )

    
    
    return render(request, 'boutiques/liste.html', {
        'boutiques': boutiques,
        'breadcrumb': [
            ('Accueil', '/'),
            ('Boutiques', None),
        ],
        
        })


def detail_boutique(request, pk):
    boutique = get_object_or_404(
        Boutique.objects.select_related('proprietaire').prefetch_related('avis_boutique'),
        id=pk,
    )
    produits = boutique.produit_set.select_related('categorie').all()
    moyenne = boutique.avis_boutique.aggregate(Avg('note'))['note__avg']

    return render(request, 'boutiques/detail.html', {
        'boutique': boutique,
        'produits': produits,
        'moyenne': moyenne,
        'breadcrumb': [
            ('Accueil', '/'),
            ('Boutiques', '/boutiques/'),
            (boutique.nom, None),
        ],
    })


@login_required
def creer_boutique(request):
    if request.user.type_user != "vendeur":
        return redirect('/')

    boutique_existante = Boutique.objects.filter(proprietaire=request.user).first()

    if boutique_existante:
        return redirect('/dashboard/')

    if request.method == "POST":
        form = BoutiqueForm(request.POST, request.FILES)

        if form.is_valid():
            boutique = form.save(commit=False)
            boutique.proprietaire = request.user
            boutique.save()
            Profil.objects.get_or_create(utilisateur=request.user)
            return redirect('/dashboard/')
    else:
        form = BoutiqueForm()

    return render(request, 'boutiques/creer.html', {'form': form})


@login_required
def ajouter_avis(request, pk):
    boutique = get_object_or_404(Boutique, id=pk)
    existe = AvisBoutique.objects.filter(boutique=boutique, utilisateur=request.user).exists()

    if existe:
        return redirect(f'/boutiques/{pk}/')

    if request.method == "POST":
        form = AvisBoutiqueForm(request.POST)

        if form.is_valid():
            avis = form.save(commit=False)
            avis.boutique = boutique
            avis.utilisateur = request.user
            avis.save()
            return redirect(f'/boutiques/{pk}/')
    else:
        form = AvisBoutiqueForm()

    return render(request, 'boutiques/avis.html', {
        'form': form,
        'boutique': boutique,
    })

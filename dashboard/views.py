from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum
from django.shortcuts import render

from boutiques.models import Boutique
from produits.models import Produit
from profil.models import Profil
from commandes.models import HistoriqueVente
from commandes.models import Commande
from django.db.models.functions import TruncMonth
import json

@login_required
def vendeur_dashboard(request):

    if request.user.type_user != "vendeur":
        return render(request, 'dashboard/interdit.html')


    boutique = Boutique.objects.filter(
        proprietaire=request.user
    ).first()


    if not boutique:
        return render(
            request,
            'dashboard/no_boutique.html'
        )


    profil, _ = Profil.objects.get_or_create(
        utilisateur=request.user
    )


    produits = Produit.objects.filter(
        boutique=boutique
    ).select_related(
        'categorie'
    ).order_by('-id')


    total_produits = produits.count()


    stock_total = produits.aggregate(
        total=Sum('stock')
    )['total'] or 0


    note_boutique = boutique.avis_boutique.aggregate(
        moyenne=Avg('note')
    )['moyenne'] or 0



    ventes = HistoriqueVente.objects.filter(
        boutique=boutique
    )

    ventes_par_mois = ventes.annotate(
        mois=TruncMonth('date_vente')
    ).values(
        'mois'
    ).annotate(
        total=Sum('montant_total')
    ).order_by(
        'mois'
    )

    produits_populaires = ventes.values(
        'produit__nom'
    ).annotate(
        total=Sum('quantite')
    ).order_by(
        '-total'
    )[:5]

    
    nombre_ventes = ventes.count()


    chiffre_affaires = ventes.aggregate(
        total=Sum('montant_total')
    )['total'] or 0



    quantite_vendue = ventes.aggregate(
        total=Sum('quantite')
    )['total'] or 0



    produits_rupture = produits.filter(
        stock__lte=5
    )


    produit_plus_vendu = None


    if ventes.exists():

        classement = ventes.values(
            'produit__nom'
        ).annotate(
            total=Sum('quantite')
        ).order_by(
            '-total'
        )

        produit_plus_vendu = classement.first()



    dernieres_ventes = ventes.order_by(
        '-date_vente'
    )[:5]


    mois_labels = []
    revenus_data = []

    produits_labels = []
    produits_quantites = []

    commandes = Commande.objects.filter(
    lignes__produit__boutique=boutique
    ).distinct()

    commandes_attente = commandes.filter(
        statut='attente'
    ).count()

    commandes_confirmees = commandes.filter(
        statut='confirmee'
    ).count()

    commandes_preparees = commandes.filter(
        statut='preparee'
    ).count()

    commandes_livrees = commandes.filter(
        statut='livree'
    ).count()


    for produit in produits_populaires:

        produits_labels.append(
            produit['produit__nom']
        )

        produits_quantites.append(
            produit['total']
        )


    for vente in ventes_par_mois:

        mois_labels.append(
            vente['mois'].strftime('%B %Y')
        )

        revenus_data.append(
            float(vente['total'])
        )

    stock_produits = produits[:5]


    stock_labels = []
    stock_values = []


    for produit in stock_produits:

        stock_labels.append(
            produit.nom
        )

        stock_values.append(
            produit.stock
        )

    mois_labels_json = json.dumps(mois_labels)

    revenus_data_json = json.dumps(revenus_data)

    produits_labels_json = json.dumps(
    produits_labels
    )

    produits_quantites_json = json.dumps(
        produits_quantites
    )


    stock_labels_json = json.dumps(
        stock_labels
    )

    stock_values_json = json.dumps(
        stock_values
    )

    
        
    return render(
        request,
        'dashboard/index.html',
        {

            'boutique': boutique,
            'profil': profil,
            'produits': produits,

            'total_produits': total_produits,
            'stock_total': stock_total,
            'note_boutique': round(note_boutique,1),

            'nombre_ventes': nombre_ventes,
            'chiffre_affaires': chiffre_affaires,
            'quantite_vendue': quantite_vendue,

            'produits_rupture': produits_rupture,

            'produit_plus_vendu': produit_plus_vendu,

            'dernieres_ventes': dernieres_ventes,

            'mois_labels': mois_labels_json,
            'revenus_data': revenus_data_json,

            'produits_labels': produits_labels_json,

            'produits_quantites': produits_quantites_json,


            'stock_labels': stock_labels_json,

            'stock_values': stock_values_json,

            'commandes_attente': commandes_attente,
            'commandes_confirmees': commandes_confirmees,
            'commandes_preparees': commandes_preparees,
            'commandes_livrees': commandes_livrees,

            'breadcrumb': [
                ('Accueil', '/'),
                ('Dashboard vendeur', None),
            ],
        }
    )

@login_required
def mes_ventes(request):

    if request.user.type_user != 'vendeur':
        return render(
            request,
            'dashboard/interdit.html'
        )

    boutique = Boutique.objects.filter(
        proprietaire=request.user
    ).first()

    ventes = HistoriqueVente.objects.filter(
        boutique=boutique
    ).order_by(
        '-date_vente'
    )

    return render(
        request,
        'dashboard/mes_ventes.html',
        {
            'ventes': ventes,
            'boutique': boutique
        ,
        'breadcrumb': [
            ('Accueil', '/'),
            ('Dashboard', '/dashboard/'),
            ('Commandes', None),
        ]}
    )

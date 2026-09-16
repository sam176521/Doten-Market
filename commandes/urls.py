from django.urls import path
from . import views

urlpatterns = [
    path(
        'passer/',
        views.passer_commande,
        name='passer_commande'
    ),

    path(
        '<int:commande_id>/',
        views.detail_commande,
        name='detail_commande'
    ),

    path(
        'mes-commandes/',
        views.mes_commandes,
        name='mes_commandes'
    ),

    path(
        'vendeur/',
        views.commandes_boutique,
        name='commandes_boutique'
    ),

    path(
        'vendeur/<int:commande_id>/',
        views.detail_commande_vendeur,
        name='detail_commande_vendeur'
    ),

    path(
        'vendeur/<int:commande_id>/<str:statut>/',
        views.modifier_statut_commande,
        name='modifier_statut_commande'
    ),
]

from django.urls import path
from . import views

urlpatterns =[
    path(
        'ajouter/<int:produit_id>/',
        views.ajouter_panier,
        name='ajouter_panier'
    ),

    path(
        '',
        views.voir_panier,
        name='voir_panier'
    ),

    path(
        'supprimer/<int:ligne_id>/',
        views.supprimer_ligne,
        name='supprimer_ligne'
    ),

    path(
        'augmenter/<int:ligne_id>/',
        views.augmenter_quantite,
        name='augmenter_quantite'
    ),

    path(
        'diminuer/<int:ligne_id>/',
        views.diminuer_quantite,
        name='diminuer_quantite'
    ),
]

from django.urls import path
from . import views

urlpatterns = [

    path('', views.liste_produits, name='liste_produits'),

    path('<int:pk>/', views.detail_produit, name='detail_produit'),

    # AJOUT PRODUIT VENDEUR
    path('ajouter/', views.ajouter_produit, name='ajouter_produit'),

    

    path('recherche/', views.rechercher_produits, name='recherche'),
    path(
    'categorie/<int:pk>/',
    views.produits_par_categorie,
    name='categorie'
),

    path(
    'modifier/<int:pk>/',
    views.modifier_produit,
    name='modifier_produit'
),

path(
    'supprimer/<int:pk>/',
    views.supprimer_produit,
    name='supprimer_produit'
),
]

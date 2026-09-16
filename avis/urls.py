from django.urls import path
from . import views

urlpatterns = [

    path(
        'ajouter/<int:pk>/',
        views.ajouter_avis,
        name='ajouter_avis_produit'
    ),

]

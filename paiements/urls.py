from django.urls import path
from . import views

urlpatterns = [

    path(
        'payer/<int:commande_id>/',
        views.payer_commande,
        name='payer_commande'
    ),

]

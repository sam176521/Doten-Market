from django.urls import path
from . import views

urlpatterns = [
    path('', views.vendeur_dashboard, name='vendeur_dashboard'),

    path('mes-ventes/',views.mes_ventes,name='mes_ventes'),
]

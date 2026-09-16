from django.urls import path
from . import views

urlpatterns = [
    path('',views.liste_boutiques, name='liste_boutiques'),
    path('<int:pk>/', views.detail_boutique, name ='detail_boutique'),
    path('creer/', views.creer_boutique, name='creer_boutique'),
    path('<int:pk>/avis/',
     views.ajouter_avis,
     name='ajouter_avis_boutique'),
]

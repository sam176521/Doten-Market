from django.urls import path
from . import views

urlpatterns = [
    path('mon-profil/', views.mon_profil, name='mon_profil')    
]

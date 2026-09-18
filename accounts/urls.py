from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path(
    'vendeur/<int:pk>/',
    views.profil_vendeur,
    name='profil_vendeur'
),
    path('creer-admin/', views.creer_admin),
]

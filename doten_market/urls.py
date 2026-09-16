"""
URL configuration for doten_market project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('admin/', admin.site.urls),

    path('', include('core.urls')),

    path('boutiques/', include('boutiques.urls')),

    path('produits/', include('produits.urls')),

    path('comparateur/', include('comparateur.urls')),

    path('accounts/', include('accounts.urls')),

    path('dashboard/', include('dashboard.urls')),

    path('commandes/', include('commandes.urls')),

    path('avis/',include('avis.urls')),
    
    path('profil/', include('profil.urls')),

    path('panier/', include('panier.urls')),

    path('notifications/',include('notifications.urls')),

    path('paiements/', include('paiements.urls')),
]


# MEDIA FILES
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

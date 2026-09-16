from django.contrib import admin
from .models import Commande, LigneCommande, HistoriqueVente

admin.site.register(Commande)
admin.site.register(LigneCommande)
admin.site.register(HistoriqueVente)
# Register your models here.

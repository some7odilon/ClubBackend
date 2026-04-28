from django.contrib import admin
from .models import User, Cotisation, Member

class AdminUser(admin.ModelAdmin):
    list_display = ('id', 'role', 'nom', 'prenom','email','password', 'member_id', 'date_inscription', 'dernier_acces', 'actif' )
    
    
class AdminMembre(admin.ModelAdmin):
    list_display = ( 'id', 'nom', 'prenoms', 'categorie', 'date_inscription', 'statut')
    

class AdminCotisation(admin.ModelAdmin):
    list_display = ( 'id', 'member', 'member_name', 'mois', 'annee', 'montant', 'date_paiement', 'statut' )
    
    
    
    
admin.site.register(User, AdminUser)
admin.site.register(Cotisation, AdminCotisation)
admin.site.register(Member, AdminMembre)

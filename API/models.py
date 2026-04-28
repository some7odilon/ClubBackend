# from django.db import models
# import uuid
# # Create your models here.

# class Transaction(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     text = models.CharField(max_length=255)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     create_at = models.DateTimeField(auto_now_add=True)
    
    
#     class Meta:
#         ordering = ['-create_at']
    
#     def __str__(self):
#         return f"{self.text}" ({self.amount})
    
    
    
from django.db import models
import uuid

# Create your models here.


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    create_at = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        ordering = ['-create_at']
    
    def __str__(self):
        return f"{self.text} ({self.amount})"
    




class Member(models.Model):
    CATEGORIE_CHOICES = [
        ('ADULTE', 'Adulte'),
        ('ENFANT', 'Enfant')
    ]
    STATUT_CHOICES = [
        ('actif', 'Actif'),
        ('inactif', 'Inactif')
    ]
    GRADE_CHOICES = [
        ('BLANCHE', 'blanche'),
        ('1ere JAUNE', '1ere jaune' ),
        ('2ieme JAUNE', '2ere jaune'),
        ('1ere VERTE', '1ere verte' ),
        ('2ieme VERTE', '2ieme verte'),
        ('1ere BLEUE', '1ere bleue' ), 
        ('2ieme BLEUE', '2ieme bleue'),
        ('3ieme BLEUE', '3ere bleue'),
        ('1ere ROUGE', '1ere rouge'), 
        ('2ieme ROUGE', '2ieme rouge'),
        ('3ieme ROUGE', '3ieme rouge'),
        ('1ere DAN', '1ere dan' ),
        ('2ieme DAN', '2ere dan'),
        ('3ieme DAN', '1ere dan')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    prenoms = models.CharField(max_length=100)
    categorie = models.CharField(max_length=10, choices=CATEGORIE_CHOICES, default='ENFANT')
    grade = models.CharField(max_length=20, choices=GRADE_CHOICES, default="BLANCHE")
    date_inscription = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='actif')
    
    class Meta:
        ordering = ['-date_inscription']
    
    def __str__(self):
        return f"{self.prenoms} {self.nom}"
    

class Cotisation(models.Model):
    MOIS_CHOICES = [
        ('Janvier', 'Janvier'), ('Février', 'Février'), ('Mars', 'Mars'),
        ('Avril', 'Avril'), ('Mai', 'Mai'), ('Juin', 'Juin'),
        ('Juillet', 'Juillet'), ('Août', 'Août'), ('Septembre', 'Septembre'),
        ('Octobre', 'Octobre'), ('Novembre', 'Novembre'), ('Décembre', 'Décembre')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='cotisations')
    member_name = models.CharField(max_length=200)
    mois = models.CharField(max_length=20, choices=MOIS_CHOICES)
    annee = models.IntegerField()
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=10, default='payé')
    
    class Meta:
        ordering = ['-date_paiement']
        unique_together = ['member', 'mois', 'annee']  # Empêche les doublons
    
    def __str__(self):
        return f"{self.member_name} - {self.mois} {self.annee}"

class Depense(models.Model):
    CATEGORIE_CHOICES = [
        ('Matériel', 'Matériel'),
        ('Location', 'Location'),
        ('Déplacement', 'Déplacement'),
        ('Compétition', 'Compétition'),
        ('Formation', 'Formation'),
        ('Autre', 'Autre')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    libelle = models.CharField(max_length=255)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_depense = models.DateTimeField(auto_now_add=True)
    categorie = models.CharField(max_length=50, choices=CATEGORIE_CHOICES)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-date_depense']
    
    def __str__(self):
        return f"{self.libelle} - {self.montant}FCFA"
    
    

class User(models.Model):
    
    ROLE_CHOICES = [
        ('membre', 'Membre'),
        ('tresorier', 'Trésorier'),
        ('president', 'Président'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='membre')
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=128, default='')
    member_id = models.IntegerField(null=True, blank=True)
    date_inscription = models.DateTimeField(auto_now_add=True)
    dernier_acces = models.DateTimeField(null=True, blank=True)
    actif = models.BooleanField(default=True)
    
    
    class Meta:
        ordering = ['-date_inscription']
        
    def __str__(self):
        return f"{self.nom} {self.prenom}"
    
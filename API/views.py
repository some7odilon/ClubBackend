
import csv
import uuid

from django.http import HttpResponse
import jwt
from django.conf import settings
import openpyxl
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Sum, Q
from datetime import datetime, timedelta
from .models import Transaction, Member, Cotisation, Depense, User
from .serialize import RegisterSerializer, TransactionSerializer, MemberSerializer, CotisationSerializer, DepenseSerializer, UserSerilizer
from django.contrib.auth.hashers import check_password
import time 
from django.utils import timezone 

# Transaction Views (garde votre code existant)
class TransactionViews(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class TransactionDeleteUpdateViews(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    lookup_field = 'id'

# Member Views
class MemberListCreateView(generics.ListCreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class MemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    lookup_field = 'id'
    
    
    
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerilizer
    lookup_field = 'id'
    
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerilizer
    lookup_field = 'id'
    
    


# Cotisation Views
class CotisationListCreateView(generics.ListCreateAPIView):
    queryset = Cotisation.objects.all()
    serializer_class = CotisationSerializer

class CotisationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cotisation.objects.all()
    serializer_class = CotisationSerializer
    lookup_field = 'id'

# Depense Views
class DepenseListCreateView(generics.ListCreateAPIView):
    queryset = Depense.objects.all()
    serializer_class = DepenseSerializer

class DepenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Depense.objects.all()
    serializer_class = DepenseSerializer
    lookup_field = 'id'

# Dashboard Statistics
@api_view(['GET'])
def dashboard_stats(request):
    # Statistiques membres
    total_membres = Member.objects.count()
    membres_actifs = Member.objects.filter(statut='actif').count()
    adultes = Member.objects.filter(categorie='ADULTE', statut='actif').count()
    enfants = Member.objects.filter(categorie='ENFANT', statut='actif').count()
    
    # Statistiques financières
    total_cotisations = Cotisation.objects.aggregate(total=Sum('montant'))['total'] or 0
    total_depenses = Depense.objects.aggregate(total=Sum('montant'))['total'] or 0
    solde = total_cotisations - total_depenses
    
    # Cotisations par mois (pour les graphiques)
    cotisations_par_mois = Cotisation.objects.values('mois', 'annee').annotate(
        total=Sum('montant')
    ).order_by('-annee', 'mois')
    
    # Dépenses par catégorie
    depenses_par_categorie = Depense.objects.values('categorie').annotate(
        total=Sum('montant')
    )
    
    # Dernières activités
    dernieres_cotisations = Cotisation.objects.all()[:5]
    dernieres_depenses = Depense.objects.all()[:5]
    
    return Response({
        'membres': {
            'total': total_membres,
            'actifs': membres_actifs,
            'adultes': adultes,
            'enfants': enfants
        },
        'finances': {
            'total_cotisations': total_cotisations,
            'total_depenses': total_depenses,
            'solde': solde
        },
        'cotisations_par_mois': list(cotisations_par_mois),
        'depenses_par_categorie': list(depenses_par_categorie),
        'dernieres_activites': {
            'cotisations': CotisationSerializer(dernieres_cotisations, many=True).data,
            'depenses': DepenseSerializer(dernieres_depenses, many=True).data
        }
    })
    

     
     
class LoginView(APIView):
    
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        
        if not email or not password:
            return Response(
                {"error": "Email et mot de passe requis"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            
            user = User.objects.get(email=email)
            if not check_password(password, user.password):
                return Response (
                    { "error": "Mot de passe incorrect"},
                    status = status.HTTP_400_BAD_REQUEST
                )
                
                
            user_str_id = str(user.id) if isinstance(user.id, uuid.UUID) else user.id 
                
            token = jwt.encode({
                
                'user_id': user_str_id,
                'email': user.email,
                'role': user.role,
                'exp': timezone.now() + timedelta(days=1)
                
            }, settings.SECRET_KEY, algorithm='HS256')
            
            user.dernier_acces = timezone.now()
            user.save()
                
                
            return Response({
                "token": token,
                "user": {
                    "id": user_str_id,
                    "nom": user.nom,
                    "prenom": user.prenom,
                    "email": user.email,
                    "role": user.role
                }
                
            })
        except User.DoesNotExist:
            return Response (
                {
                    "error": "Utilisateur non trouvé"
                },
                
                status=status.HTTP_400_BAD_REQUEST
            )
    

class RegisterView(APIView):
    
    def post(self, request):
        data = request.data.copy()
        data['role'] = 'membre'
        serializer = RegisterSerializer(data=request.data) 
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Inscription réussie",
                "user": {
                    "id": str(user.id) if isinstance(user.id, uuid.UUID) else user.id,
                    "nom": user.nom,
                    "prenom": user.prenom,
                    "email": user.email,
                    "role": user.role
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST )
    
    
class MeView(APIView):
    def get(self, request):
            
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return Response({
                "error": "Non authorisé"
            }, status=401)
            
        try:
                
                parts = auth_header.split()
                if len(parts) != 2 or parts[0].lower() != 'bearer':
                    return Response(
                        {"error": "Format de token invalide. Utilisez 'Bearer <token>'"},
                        status=status.HTTP_401_UNAUTHORIZED
                    )
            
                token = parts[1]
                
                payload = jwt.decode(
                    token, settings.SECRET_KEY, algorithms=['HS256']
                )
                
                user = User.objects.get(id=payload['user_id'], actif=True)
                
                return Response({
                    
                "id": str(user.id) if isinstance(user.id, uuid.UUID) else user.id,
                "nom": user.nom,
                "prenom": user.prenom, 
                "email": user.email,
                "role": user.role,
                "actif": user.actif,
                "date_inscription": user.date_inscription
                    
                })
                
                
        except jwt.ExpiredSignatureError:
                return Response(
                    { "error": "Token expiré" },
                    status=status.HTTP_401_UNAUTHORIZED
                )
                
                
        except jwt.InvalidTokenError:
                return Response(
                    { "error": "token invalide"},
                    status=status.HTTP_401_UNAUTHORIZED
                    
                )
                
        except User.DoesNotExist:
                return Response(
                    {"error": "Utilisateur non trouvé"},
                    status=status.HTTP_404_NOT_FOUND
                )
        except Exception as e:
                print(f"Erreur MeView: {str(e)}")
                return Response(
                    {"error": "Erreur d'authentification"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
              
              
class AdminStatsView(APIView):
    def get(self, request):
        # Vérifier token et permission président
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return Response({"error": "Non autorisé"}, status=401)
        
        try:
            token = auth_header.split()[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            
            if payload['role'] != 'president':
                return Response({"error": "Permission refusée"}, status=403)
            
            # Statistiques utilisateurs
            now = timezone.now()
            first_day_month = now.replace(day=1, hour=0, minute=0, second=0)
            
            total_users = User.objects.count()
            active_users = User.objects.filter(actif=True).count()
            new_users_this_month = User.objects.filter(
                date_inscription__gte=first_day_month
            ).count()
            
            total_membres = User.objects.filter(role='membre').count()
            total_tresoriers = User.objects.filter(role='tresorier').count()
            
            # Statistiques financières
            total_cotisations = Cotisation.objects.filter(
                statut='payé'
            ).aggregate(total=Sum('montant'))['total'] or 0
            
            total_depenses = Depense.objects.aggregate(
                total=Sum('montant')
            )['total'] or 0
            
            solde_caisse = total_cotisations - total_depenses
            
            return Response({
                'totalUsers': total_users,
                'activeUsers': active_users,
                'newUsersThisMonth': new_users_this_month,
                'totalMembres': total_membres,
                'totalTresoriers': total_tresoriers,
                'totalCotisations': float(total_cotisations),
                'totalDepenses': float(total_depenses),
                'soldeCaisse': float(solde_caisse)
            })
            
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class ExportDataView(APIView):
    def get(self, request):
        format_type = request.GET.get('format', 'csv')
        
        users = User.objects.all().values(
            'id', 'nom', 'prenom', 'email', 'role', 'actif', 'date_inscription'
        )
        
        if format_type == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="export_{timezone.now().date()}.csv"'
            
            writer = csv.writer(response)
            writer.writerow(['ID', 'Nom', 'Prénom', 'Email', 'Rôle', 'Actif', 'Date inscription'])
            
            for user in users:
                writer.writerow([
                    user['id'], user['nom'], user['prenom'], 
                    user['email'], user['role'], user['actif'], 
                    user['date_inscription']
                ])
            
            return response
        
        elif format_type == 'excel':
            response = HttpResponse(
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename="export_{timezone.now().date()}.xlsx"'
            
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Utilisateurs"
            
            # En-têtes
            headers = ['ID', 'Nom', 'Prénom', 'Email', 'Rôle', 'Actif', 'Date inscription']
            ws.append(headers)
            
            # Données
            for user in users:
                ws.append([
                    user['id'], user['nom'], user['prenom'], 
                    user['email'], user['role'], user['actif'], 
                    user['date_inscription']
                ])
            
            wb.save(response)
            return response
        
        return Response({"error": "Format non supporté"}, status=400)  
                



from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password

@csrf_exempt
def create_admin(request):
    if request.method == 'POST':
        try:
            # Vérifie si l'admin existe déjà
            if not User.objects.filter(username='admin').exists():
                User.objects.create(
                    username='admin',
                    email='admin@club.com',
                    password=make_password('MotDePasseAdmin123'),
                    is_superuser=True,
                    is_staff=True
                )
                return JsonResponse({'message': 'Admin créé avec succès'}, status=201)
            else:
                return JsonResponse({'message': 'Admin existe déjà'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

from rest_framework import serializers
from .models import Transaction, Member, Cotisation, Depense, User
from django.contrib.auth.hashers import make_password

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'text', 'amount', 'create_at']
        read_only_fields = ['id', 'create_at']

# class MemberSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Member
#         fields = ['id', 'nom', 'prenoms', 'categorie', 'date_inscription', 'statut']
#         read_only_fields = ['id', 'date_inscription']

# class TransactionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Transaction
#         fields = ['id', 'text', 'amount', 'create_at']
#         read_only_fields = ['id', 'create_at']

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'nom', 'prenoms', 'categorie', 'grade', 'date_inscription', 'statut']
        read_only_fields = ['id', 'date_inscription']

class CotisationSerializer(serializers.ModelSerializer):
    member_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = Cotisation
        fields = ['id', 'member', 'member_id', 'member_name', 'mois', 'annee', 'montant', 'date_paiement', 'statut']
        read_only_fields = ['id', 'date_paiement', 'member_name', 'member']
        
    def create(self, validated_data):
        member_id = validated_data.pop('member_id')
        
        try:
            member = Member.objects.get(id=member_id)
        except Member.DoesNotExist:
            raise serializers.ValidationError({
                "member_id": "Membre introuvable"
            })
        
        
        validated_data['member'] = member
        validated_data['member_name'] = f"{member.prenoms} {member.nom}"
        
        return super().create(validated_data)
        

class DepenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Depense
        fields = ['id', 'libelle', 'montant', 'date_depense', 'categorie', 'description']
        read_only_fields = ['id', 'date_depense']
        
    

class UserSerilizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'role', 'nom', 'prenom', 'email', 'member_id', 'date_inscription', 'dernier_acces', 'actif']
        read_only_fields = ['id', 'date_inscription']
        
        



class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nom', 'prenom', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    
    
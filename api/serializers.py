# api/serializers.py
from rest_framework import serializers
from myauth.models import User
from .models import Organisation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userId', 'firstName', 'lastName', 'email', 'phone']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['userId'] = str(instance.userId)  # Ensure UUID is converted to string
        return rep
 
# class OrganisationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Organisation
#         fields = ['org_id', 'name', 'description']


# class OrganisationCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Organisation
#         fields = ['name', 'description']

#     def create(self, validated_data):
#         Organisation = Organisation.objects.create(**validated_data)
#         return Organisation
    
class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ['org_id', 'name', 'description']

class OrganisationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ['name', 'description']

class AddUserToOrganisationSerializer(serializers.Serializer):
    userId = serializers.CharField()

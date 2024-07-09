from rest_framework import serializers
from .models import User
from api.models import Organisation
import uuid
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True) # validators=[validate_password]
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    firstName = serializers.CharField(
        required=True,
    )
    lastName = serializers.CharField(
        required=True,
    )
    phone = serializers.CharField(required=True,)

    class Meta:
        model = User
        fields = ('firstName', 'lastName', 'email', 'password', 'phone')

    def create(self, validated_data):
        user = User.objects.create(
            userId=str(uuid.uuid4()),
            firstName=validated_data['firstName'],
            lastName=validated_data['lastName'],
            email=validated_data['email'],
            phone=validated_data['phone']
        )

        user.set_password(validated_data['password'])
        user.save()
                

        org_name = f"{user.firstName}'s Organisation"
        organisation = Organisation.objects.create(
            org_id=str(uuid.uuid4()),
            name=org_name,
            description=f""
        )
        organisation.users.add(user)
        
        organisation.save()

        return user




class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['userId'] = str(user.userId)
        token['firstName'] = user.firstName
        token['lastName'] = user.lastName
        token['email'] = user.email
        token['phone'] = user.phone

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Remove the refresh token
        data.pop('refresh', None)

        # Reformat the response
        formatted_data = {
            "status": "success",
            "message": "Login successful",
            "data": {
                "accessToken": data.pop('access'),
                "user": {
                    "userId": str(self.user.userId),
                    "firstName": self.user.firstName,
                    "lastName": self.user.lastName,
                    "email": self.user.email,
                    "phone": self.user.phone,
                }
            }
        }

        return formatted_data
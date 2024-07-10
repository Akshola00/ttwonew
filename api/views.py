# api/views.py
import uuid
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from myauth.models import User
from .models import Organisation
from .serializers import UserSerializer, OrganisationSerializer, OrganisationCreateSerializer, AddUserToOrganisationSerializer
from rest_framework.exceptions import PermissionDenied, NotFound


class OrganisationView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, org_id=None, *args, **kwargs):
        if org_id:
            return self.get_single_organisation(request, org_id)
        else:
            return self.get_all_organisations(request)

    def post(self, request, org_id=None, *args, **kwargs):
        if org_id:
            return self.add_user_to_organisation(request, org_id)
        else:
            return self.create_organisation(request)

    def get_all_organisations(self, request):
        organisations = Organisation.objects.filter(users=request.user)
        serializer = OrganisationSerializer(organisations, many=True)
        response_data = {
            "status": "success",
            "message": "Organisations retrieved successfully",
            "data": {
                "organisations": serializer.data
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def get_single_organisation(self, request, org_id):
        try:
            organisation = Organisation.objects.get(org_id=org_id, users=request.user)
        except Organisation.DoesNotExist:
            raise NotFound("Organisation not found or you do not have access to it.")

        serializer = OrganisationSerializer(organisation)
        response_data = {
            "status": "success",
            "message": "Organisation retrieved successfully",
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def create_organisation(self, request):
        serializer = OrganisationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        organisation = serializer.save(org_id=uuid.uuid4())
        organisation.users.add(request.user)  # Add the creator to the organisation

        response_data = {
            "status": "success",
            "message": "Organisation created successfully",
            "data": {
                "org_id":  organisation.org_id,
                "name": organisation.name,
                "description": organisation.description
            }
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

    def add_user_to_organisation(self, request, org_id):
        try:
            organisation = Organisation.objects.get(org_id=org_id)
        except Organisation.DoesNotExist:
            raise NotFound("Organisation not found.")

        serializer = AddUserToOrganisationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(userId=serializer.validated_data['userId'])  # Use userId here
        organisation.users.add(user)

        response_data = {
            "status": "success",
            "message": "User added to organisation successfully",
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['pk']
        print(f"User ID received: {user_id}")  # Debugging line
        try:
            # Fetch the user based on string ID
            user = User.objects.get(userId=user_id)
            if request.user == user or request.user.organisations.filter(id=user_id).exists():
                serializer = self.get_serializer(user)
                return Response({
                    "status": "success",
                    "message": "User retrieved successfully",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": "error",
                    "message": "You do not have permission to view this user",
                    "statusCode": 403
                }, status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response({
                "status": "error",
                "message": "User not found",
                "statusCode": 404
            }, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({
                "status": "error",
                "message": "Invalid user ID format",
                "statusCode": 400
            }, status=status.HTTP_400_BAD_REQUEST)
# class UserDetailView(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]
#     lookup_field = 'pk'

#     def get(self, request, *args, **kwargs):
#         user_id = self.kwargs['pk']
#         user = self.get_object()
#         if request.user == user or request.user.organisations.filter(id=user_id).exists():
#             serializer = self.get_serializer(user)
#             return Response({
#                 "status": "success",
#                 "message": "User retrieved successfully",
#                 "data": serializer.data
#             }, status=status.HTTP_200_OK)
#         else:
#             return Response({
#                 "status": "error",
#                 "message": "You do not have permission to view this user",
#                 "statusCode": 403
#             }, status=status.HTTP_403_FORBIDDEN)
   
 
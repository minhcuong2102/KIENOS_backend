from django.shortcuts import get_object_or_404
from rest_framework import viewsets, renderers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models.customer_profile import CustomerProfile
from ..serializers.user_profile import CustomerProfileSerializer, CreateCustomerProfileSerializer, CoachProfileShortSerializer
from base.utils.custom_pagination import CustomPagination
from rest_framework.decorators import action
from user.models.user import User
from base.permissions import IsAdmin
from user.serializers.user import UserProfileSerializer
from user_profile.models.coach_profile import CoachProfile
from service.models.contract import Contract
from base.permissions import IsCustomer
from django.conf import settings
from urllib.parse import urlparse
import cloudinary
from cloudinary import CloudinaryImage
import cloudinary.uploader
import cloudinary.api
from dotenv import load_dotenv
load_dotenv()

class CustomerProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomerProfile.objects.all().order_by('id')
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return CustomerProfileSerializer
        if self.action == 'create' or self.action in ['update', 'partial_update']:
            return CreateCustomerProfileSerializer
        return CustomerProfileSerializer 

    def create(self, request, *args, **kwargs):
        user = request.user

        user_data = {
            'avatar_url': request.data.get('avatar_url'),
            'phone': request.data.get('phone'),
            'email': request.data.get('email')
        }
        user_serializer = UserProfileSerializer(user, data=user_data, partial=True)

        if user_serializer.is_valid():
            user_serializer.save()
            workout_goal = {
                'general': request.data.get('general'),
                'weight': request.data.get('goal_weight'),
                'muscle_mass': request.data.get('goal_muscle_mass'),
                'body_fat': request.data.get('goal_body_fat'),
            }
            profile_data = {
                'first_name': request.data.get('first_name'),
                'last_name': request.data.get('last_name'),
                'address': request.data.get('address'),
                'gender': request.data.get('gender'),
                'birthday': request.data.get('birthday'),
                'height': request.data.get('height'),
                'weight': request.data.get('weight'),
                'workout_goal': workout_goal,
            }

            profile_data['customer'] = request.user.id
            
            profile_serializer = self.get_serializer(data=profile_data)

            if profile_serializer.is_valid():
                profile_serializer.save(customer=user)
                # cloudinary.config(cloud_name = settings.CLOUDINARY_URL, api_key=settings.CLOUD_API, api_secret=settings.CLOUD_SECRET)
                # cloudinary.uploader.upload(request.data.get('avatar_url'))
                return Response({'message': 'Profile created successfully!'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'profile_errors': profile_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'user_errors': user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False) 
        instance = self.get_object()  
        user_data = {
            'phone': request.data.get('phone'),
            'email': request.data.get('email')
        }

        if 'avatar_url' in request.data and isinstance(request.data['avatar_url'], str) and request.data['avatar_url'].startswith('http'):
            user_data['avatar_url'] = instance.customer.avatar_url
        else:
            user_data['avatar_url'] = request.data.get('avatar_url')
            # cloudinary.config(cloud_name="dzcvenbcx", api_key=settings.CLOUD_API, api_secret=settings.CLOUD_SECRET)
            config = cloudinary.config(secure=True)
            print("Credentials: ", config.cloud_name, config.api_key, "\n")
            # print(request.data.get('avatar_url'))
            upload_result = cloudinary.uploader.upload(request.data.get('avatar_url'))
            full_url = upload_result['secure_url']
            parsed_url = urlparse(upload_result['secure_url'])
            short_url = parsed_url.path 
            user_data['avatar_url'] = short_url
            
        user_serializer = UserProfileSerializer(instance.customer, data=user_data, partial=partial)

        if user_serializer.is_valid():
            user_serializer.save()
            workout_goal = {
                'general': request.data.get('general'),
                'weight': request.data.get('goal_weight'),
                'muscle_mass': request.data.get('goal_muscle_mass'),
                'body_fat': request.data.get('goal_body_fat'),
            }
            profile_data = {
                'first_name': request.data.get('first_name'),
                'last_name': request.data.get('last_name'),
                'address': request.data.get('address'),
                'gender': request.data.get('gender'),
                'birthday': request.data.get('birthday'),
                'height': request.data.get('height'),
                'weight': request.data.get('weight'),
                'workout_goal': workout_goal,
            }

            profile_serializer = CreateCustomerProfileSerializer(instance, data=profile_data, partial=partial)

            if profile_serializer.is_valid():
                profile_serializer.save()
                return Response({'message': 'Profile updated successfully!'}, status=status.HTTP_200_OK)
            else:
                return Response({'profile_errors': profile_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'user_errors': user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    

    @action(methods=['put', 'patch'], detail=True, permission_classes=[IsAdmin])
    def update_fields(self, request, pk=None):
        customer_profile = self.get_object()
        coach_id = request.data.get('coach')

        serializer = CustomerProfileSerializer(customer_profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            if coach_id:
                try:
                    coach = CoachProfile.objects.get(pk=coach_id)

                    Contract.objects.filter(customer=customer_profile).update(coach=coach)
                    return Response({
                        "message": "Customer updated successfully, including coach change.",
                        "customer_data": serializer.data
                    }, status=status.HTTP_200_OK)
                except CoachProfile.DoesNotExist:
                    return Response({
                        "error": "Coach does not exist."
                    }, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], url_path='get-coachs', detail=False, permission_classes=[IsAuthenticated], 
            renderer_classes=[renderers.JSONRenderer])  
    def get_coachs(self, request):
        try:
            customer_profile = CustomerProfile.objects.get(customer=request.user)
            
            contracts = Contract.objects.filter(
                customer=customer_profile,
                ptservice__isnull=False,
                is_purchased=True,
            )
            
            if not contracts:
                return Response({"message": "No contracts found with this this customer!"}, status=status.HTTP_404_NOT_FOUND)
            
            coachs_data = []
        
            for contract in contracts:
                coach = contract.coach 
                coach_data = CoachProfileShortSerializer(coach).data
                coach_data['contract_id'] = contract.id 
                coachs_data.append(coach_data)
            
            return Response({
                'coachs': coachs_data
            })
        except CustomerProfile.DoesNotExist:
            return Response({"error": "Customer profile not found"}, status=status.HTTP_404_NOT_FOUND)

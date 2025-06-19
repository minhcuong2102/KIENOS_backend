from django.shortcuts import get_object_or_404
from rest_framework import viewsets, renderers
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from ..models.coach_profile import CoachProfile
from ..serializers.user_profile import CoachProfileSerializer
from base.utils.custom_pagination import CustomPagination
from rest_framework.decorators import action
from user.serializers.user import UserProfileSerializer
from user_profile.models.customer_profile import CustomerProfile
from user_profile.serializers.user_profile import CustomerProfileSerializer, CreateCoachProfileSerializer, CustomerProfileShortSerializer, CoachProfileShortSerializer
from rest_framework.permissions import IsAuthenticated
from base.permissions import IsCoach
from service.models.contract import Contract
from service.serializers.contract import ContractSerializer
from django.db.models import F
from django.utils import timezone
from base.permissions import IsAdmin, IsCoach, IsSale

class CoachProfileViewSet(viewsets.ModelViewSet):
    queryset = CoachProfile.objects.all().order_by('id')
    permission_classes = [IsAuthenticated]
    serializer_class = CoachProfileSerializer
    # pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return CoachProfileSerializer
        if self.action == 'create' or self.action in ['update', 'partial_update']:
            return CoachProfileSerializer

    def create(self, request):
        user = request.user
        config = cloudinary.config(secure=True)
        print("Credentials: ", config.cloud_name, config.api_key, "\n")
        upload_result = cloudinary.uploader.upload(request.data.get('avatar_url'))
        full_url = upload_result['secure_url']
        parsed_url = urlparse(upload_result['secure_url'])
        short_url = parsed_url.path 
        print(short_url)
        # user_data['avatar_url'] = full_url
        user_data = {
            'avatar_url': full_url,
            'phone': request.data.get('phone'),
            'email': request.data.get('email'),
        }

        user_serializer = UserProfileSerializer(user, data=user_data)

        if user_serializer.is_valid():
            user_serializer.save()  
            
            profile = {
                'first_name': request.data.get('first_name'),
                'last_name': request.data.get('last_name'),
                'address': request.data.get('address'),
                'gender': request.data.get('gender'),
                'birthday': request.data.get('birthday'),
                'height': request.data.get('height'),
                'weight': request.data.get('weight'),
                'coach': request.user.id,
                'experiences': request.data.get('experiences'),
            }
            
            profile_serializer = CreateCoachProfileSerializer(data=profile)

            if profile_serializer.is_valid():
                profile_serializer.save(coach=user)
                
                return Response({'message': 'Create profile successfully!'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'profile_errors': profile_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'user_errors': user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False) 
        instance = self.get_object()  

        user_data = {
            'phone': request.data.get('phone'),
            'email': request.data.get('email'),
        }

        if 'avatar_url' in request.data and isinstance(request.data['avatar_url'], str) and request.data['avatar_url'].startswith('http'):
            user_data['avatar_url'] = instance.coach.avatar_url
        else:
            user_data['avatar_url'] = request.data.get('avatar_url')
            config = cloudinary.config(secure=True)
            print("Credentials: ", config.cloud_name, config.api_key, "\n")
            upload_result = cloudinary.uploader.upload(request.data.get('avatar_url'))
            full_url = upload_result['secure_url']
            parsed_url = urlparse(upload_result['secure_url'])
            short_url = parsed_url.path 
            print(short_url)
            user_data['avatar_url'] = full_url

        user_serializer = UserProfileSerializer(instance.coach, data=user_data, partial=partial)

        if user_serializer.is_valid():
            user_serializer.save()

            profile_data = {
                'first_name': request.data.get('first_name'),
                'last_name': request.data.get('last_name'),
                'address': request.data.get('address'),
                'gender': request.data.get('gender'),
                'birthday': request.data.get('birthday'),
                'height': request.data.get('height'),
                'weight': request.data.get('weight'),
                'experiences': request.data.get('experiences'),
            }

            profile_serializer = CoachProfileSerializer(instance, data=profile_data, partial=partial)

            if profile_serializer.is_valid():
                profile_serializer.save()
                return Response({'message': 'Update profile successfully!'}, status=status.HTTP_200_OK)
            else:
                return Response({'profile_errors': profile_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'user_errors': user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        

    @action(methods=['get'], url_path='details', detail=False, permission_classes=[IsAuthenticated, IsCoach], 
            renderer_classes=[renderers.JSONRenderer])  
    def details(self, request):
        try:
            coach_profile = CoachProfile.objects.get(coach=request.user)
            
            contracts = Contract.objects.filter(
                coach=coach_profile,
                ptservice__isnull=False,
                # used_sessions__lt=F('number_of_session'),
                is_purchased=True,
                expire_date__gt=timezone.now().date(),
            )
            
            if not contracts:
                return Response({"error": "No contracts found with this this coach!"}, status=status.HTTP_404_NOT_FOUND)
            
            customers = CustomerProfile.objects.filter(customer_contracts__in=contracts).distinct()
            
            customers_serializer = CustomerProfileSerializer(customers, many=True)
            coach_contracts_serializer = ContractSerializer(contracts, many=True)
            
            return Response({
                # 'customers': customers_serializer.data,
                'coach_contracts': coach_contracts_serializer.data,
            })
        except CoachProfile.DoesNotExist:
            return Response({"error": "Coach profile not found"}, status=status.HTTP_404_NOT_FOUND)
        

    @action(methods=['get'], url_path='get-customers', detail=False, permission_classes=[IsAuthenticated, IsCoach], 
            renderer_classes=[renderers.JSONRenderer])  
    def get_customers(self, request):
        try:
            coach_profile = CoachProfile.objects.get(coach=request.user)
            
            contracts = Contract.objects.filter(
                coach=coach_profile,
                ptservice__isnull=False,
                # used_sessions__lt=F('number_of_session'),
                is_purchased=True,
                expire_date__gt=timezone.now().date(),
            )
            
            if not contracts:
                return Response({"message": "No contracts found with this this coach!"}, status=status.HTTP_404_NOT_FOUND)
            
            customers_data = []
        
            for contract in contracts:
                customer = contract.customer  # assuming each contract has a foreign key to `customer`
                customer_data = CustomerProfileShortSerializer(customer).data
                customer_data['contract_id'] = contract.id  # add the `contract_id` for each customer
                customers_data.append(customer_data)
            
            return Response({
                'coach_id': coach_profile.id,
                'customers': customers_data
            })
        except CoachProfile.DoesNotExist:
            return Response({"error": "Coach profile not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['get'], url_path='all', detail=False, permission_classes=[IsAuthenticated], 
            renderer_classes=[renderers.JSONRenderer])  
    def all(self, request):
        coach_profiles = self.queryset
        serializer = CoachProfileShortSerializer(coach_profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

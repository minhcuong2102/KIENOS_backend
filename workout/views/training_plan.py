from django.shortcuts import get_object_or_404
from rest_framework import viewsets, renderers
from rest_framework.permissions import AllowAny, IsAuthenticated
from service.models.contract import Contract
from user_profile.models.customer_profile import CustomerProfile
from base.permissions import IsCoachOrCustomer, IsCoach
from rest_framework.response import Response
from rest_framework import status
from workout.models.training_plan import TrainingPlan
from base.utils.custom_pagination import CustomPagination
from rest_framework.decorators import action
from user.models.user import User
from ..serializers.training_plan import TrainingPlanSerializer, EditTrainingPlanSerializer
from user_profile.models.coach_profile import CoachProfile
from django.db.models import F
from base.permissions import IsAdmin

class TrainingPlanViewSet(viewsets.ModelViewSet):
    queryset = TrainingPlan.objects.all().order_by('id')
    permission_classes = [IsCoachOrCustomer | IsAdmin]
    # serializer_class = WorkoutScheduleSerializer
    # pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return TrainingPlanSerializer
        if self.action == 'create':
            return EditTrainingPlanSerializer
        if self.action in ['update', 'partial_update']:
            return EditTrainingPlanSerializer
        return TrainingPlanSerializer 
    
    @action(methods=['get'], url_path='get-by-customers', detail=False, permission_classes=[IsAuthenticated | IsCoach], 
            renderer_classes=[renderers.JSONRenderer])
    def get_by_customers(self, request):
        try:
            coach_profile = CoachProfile.objects.get(coach=request.user)
            
            contracts = Contract.objects.filter(
                coach=coach_profile,
                ptservice__isnull=False,
                used_sessions__lt=F('number_of_session')
            )
            
            customers = CustomerProfile.objects.filter(customer_contracts__in=contracts).distinct()
            
            training_plans = TrainingPlan.objects.filter(customer__in=customers)

            customer = request.query_params.get('customer')
            if customer:
                training_plans = training_plans.filter(customer=customer)

            training_plan_serializer = TrainingPlanSerializer(training_plans, many=True)

            return Response({
                'training_plans' :training_plan_serializer.data
            })
        except CoachProfile.DoesNotExist:
            return Response({"error": "Training plan(s) not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['put', 'patch'], detail=True, permission_classes=[IsCoach])
    def update_fields(self, request, pk=None):
        exercise = self.get_object()
        serializer = EditTrainingPlanSerializer(exercise, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='delete-multiple', permission_classes=[IsCoach])
    def delete_multiple(self, request):
        tp_ids = request.data.get('ids', [])
        if not tp_ids:
            return Response({'error': 'No ID(s) found!'}, status=status.HTTP_400_BAD_REQUEST)
        
        tps = TrainingPlan.objects.filter(id__in=tp_ids)
        
        if not tps.exists():
            return Response({'error': 'Can not found training plan(s) with provided ID(s)!'}, status=status.HTTP_404_NOT_FOUND)
        
        deleted_count, _ = tps.delete()
        
        return Response({'message': f'Deleted {deleted_count} training plan(s) successfully!'}, status=status.HTTP_200_OK)
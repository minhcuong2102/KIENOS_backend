from django.shortcuts import get_object_or_404
from rest_framework import viewsets, renderers
from rest_framework.permissions import AllowAny, IsAuthenticated
from base.permissions import IsCoachOrCustomer, IsCoach
from rest_framework.response import Response
from rest_framework import status
from workout.models.workout_schedule import WorkoutSchedule
from base.utils.custom_pagination import CustomPagination
from rest_framework.decorators import action
from user.models.user import User
from ..serializers.workout_schedule import WorkoutScheduleSerializer, EditWorkoutScheduleSerializer, CustomWorkoutScheduleSerializer
from ..serializers.training_plan import EditTrainingPlanSerializer
from ..models.training_plan import TrainingPlan
from user_profile.models.customer_profile import CustomerProfile
from user_profile.models.coach_profile import CoachProfile
from ..models.exercise import Exercise
from base.permissions import IsAdmin, IsCoach, IsCustomer
import json
from django.utils import timezone
from datetime import timedelta
from django.utils.dateparse import parse_datetime

class WorkoutScheduleViewSet(viewsets.ModelViewSet):
    queryset = WorkoutSchedule.objects.all().order_by('id')
    permission_classes = [IsCoachOrCustomer]
    # serializer_class = WorkoutScheduleSerializer
    # pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return WorkoutScheduleSerializer
        if self.action == 'create':
            return EditWorkoutScheduleSerializer
        if self.action in ['update', 'partial_update']:
            return EditWorkoutScheduleSerializer
        return WorkoutScheduleSerializer 
    
    def list(self, request):
        user = request.user
        if user.role.name == 'coach':
            coach_profile = user.coach_profile
            contracts = coach_profile.coach_contracts.filter(
                ptservice__isnull=False,
                is_purchased =True,
                expire_date__gte=timezone.now().date(),
            )
            
            customers = contracts.values_list('customer', flat=True)

            workout_schedule = WorkoutSchedule.objects.filter(
                coach=coach_profile, 
                customer__in=customers
            ).all().order_by('-end_time')
        
        if user.role.name == 'customer':
            customer_profile = user.customer_profile
            coach_of_user = customer_profile.customer_contracts.filter(
                ptservice__isnull=False, 
                is_purchased=True,
                expire_date__gte=timezone.now().date()   
            ).first().coach

            workout_schedule = WorkoutSchedule.objects.filter(customer=customer_profile, coach=coach_of_user).all().order_by('-end_time')
        
        serializer = WorkoutScheduleSerializer(workout_schedule, many=True)
        
        return Response(serializer.data)
    
    # def create(self, request, *args, **kwargs):
    #     serializer = EditWorkoutScheduleSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)

    #     training_plan_data = serializer.validated_data.pop('training_plan')
    #     try:
    #         training_plan = TrainingPlan.objects.get(id=training_plan_data['id'])

    #         for key, value in training_plan_data.items():
    #             if key != 'exercises':
    #                 setattr(training_plan, key, value)

    #         exercise_ids = [exercise['id'] for exercise in training_plan_data['exercises']]
    #         training_plan.exercises.set(Exercise.objects.filter(pk__in=exercise_ids))
    #     except TrainingPlan.DoesNotExist:
    #         return Response({'message': 'Training plan not found!'}, status=status.HTTP_404_NOT_FOUND)

    #     training_plan.save()

    #     workout_schedule = WorkoutSchedule.objects.create(**serializer.validated_data, training_plan=training_plan)
    #     workout_schedule_serializer = WorkoutScheduleSerializer(workout_schedule)

    #     return Response(workout_schedule_serializer.data, status=status.HTTP_201_CREATED)
    def create(self, request, *args, **kwargs):
        serializer = EditWorkoutScheduleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        training_plan_data = serializer.validated_data.pop('training_plan')
        try:
            training_plan = TrainingPlan.objects.get(id=training_plan_data['id'])

            for key, value in training_plan_data.items():
                if key != 'exercises':
                    setattr(training_plan, key, value)

            exercise_ids = [exercise['id'] for exercise in training_plan_data['exercises']]
            training_plan.exercises.set(Exercise.objects.filter(pk__in=exercise_ids))
        except TrainingPlan.DoesNotExist:
            return Response({'message': 'Training plan not found!'}, status=status.HTTP_404_NOT_FOUND)

        training_plan.save()

        # 🟡 Lấy số ngày lặp lại (0 = không lặp)
        repeat_days = int(request.data.get('repeat_days', 0))

        # 🟡 Chuẩn bị danh sách lịch sẽ tạo
        schedules = []

        # 🟡 Lặp để tạo từng buổi theo ngày
        for i in range(repeat_days + 1):  # +1 để bao gồm cả ngày đầu tiên
            new_data = serializer.validated_data.copy()

            # Tăng start_time, end_time theo ngày
            new_data['start_time'] += timedelta(days=i)
            new_data['end_time'] += timedelta(days=i)

            workout_schedule = WorkoutSchedule.objects.create(
                **new_data,
                training_plan=training_plan
            )
            schedules.append(workout_schedule)

        # 🟢 Trả về danh sách tất cả lịch đã tạo
        return Response(
            WorkoutScheduleSerializer(schedules, many=True).data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, pk, *args, **kwargs):
        try:
            workout_schedule = WorkoutSchedule.objects.get(pk=pk)
        except WorkoutSchedule.DoesNotExist:
            return Response({'message': 'Workout schedule not found!'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EditWorkoutScheduleSerializer(workout_schedule, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        training_plan_data = serializer.validated_data.pop('training_plan', None)

        training_plan = None

        if training_plan_data:
            try:
                training_plan = TrainingPlan.objects.get(id=training_plan_data['id'])

                for key, value in training_plan_data.items():
                    if key != 'exercises':
                        setattr(training_plan, key, value)

                exercise_ids = [exercise['id'] for exercise in training_plan_data['exercises']]
                training_plan.exercises.set(Exercise.objects.filter(pk__in=exercise_ids))
                training_plan.save()

            except TrainingPlan.DoesNotExist:
                return Response({'message': 'Training plan not found!'}, status=status.HTTP_404_NOT_FOUND)

        for key, value in serializer.validated_data.items():
            setattr(workout_schedule, key, value)

        if training_plan:
            workout_schedule.training_plan = training_plan

        workout_schedule.save()
        
        workout_schedule_serializer = WorkoutScheduleSerializer(workout_schedule)
        return Response(workout_schedule_serializer.data, status=status.HTTP_200_OK)


    @action(methods=['put', 'patch'], url_path='update-fields', detail=True, permission_classes=[IsCoach | IsCustomer | IsAdmin], 
        renderer_classes=[renderers.JSONRenderer]) 
    def update_fields(self, request, pk, *args, **kwargs):
        try:
            workout_schedule = WorkoutSchedule.objects.get(pk=pk)
        except WorkoutSchedule.DoesNotExist:
            return Response({'message': 'Workout schedule not found!'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EditWorkoutScheduleSerializer(workout_schedule, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        tp_data = request.data['training_plan']
        print("22222", tp_data)

        training_plan_data = json.loads(tp_data)

        if training_plan_data:
            try:
                training_plan = TrainingPlan.objects.get(id=int(training_plan_data['id']))

                for key, value in training_plan_data.items():
                    if key not in ['exercises', 'customer']:
                        setattr(training_plan, key, value)

                exercise_ids = [exercise['id'] for exercise in training_plan_data['exercises']]
                training_plan.exercises.set(Exercise.objects.filter(pk__in=exercise_ids))
                cus_profile = CustomerProfile.objects.get(id=training_plan_data['customer']['id'])
                training_plan.customer = cus_profile
                training_plan.save()

            except TrainingPlan.DoesNotExist:
                return Response({'message': 'Training plan not found!'}, status=status.HTTP_404_NOT_FOUND)
            
        for key, value in serializer.validated_data.items():
            setattr(workout_schedule, key, value)

        workout_schedule.training_plan = training_plan
        workout_schedule.save()
        
        workout_schedule_serializer = WorkoutScheduleSerializer(workout_schedule)
        return Response(workout_schedule_serializer.data, status=status.HTTP_200_OK)
    

    # @action(methods=['post'], url_path='create-new', detail=False, permission_classes=[IsCoach | IsCustomer | IsAdmin], 
    #     renderer_classes=[renderers.JSONRenderer]) 
    # def create_new(self, request, *args, **kwargs):
    #     ws_data = {
    #         'start_time': request.data.get('start_time', [None]),
    #         'end_time': request.data.get('end_time', [None]),
    #         'customer': request.data.get('customer', [None]),
    #         'coach': request.user.coach_profile.id
    #     }
                
    #     serializer = CustomWorkoutScheduleSerializer(data=ws_data)
    #     serializer.is_valid(raise_exception=True)

    #     tp_data = request.data['training_plan']

    #     training_plan_data = json.loads(tp_data)

    #     if training_plan_data:
    #         try:
    #             training_plan = TrainingPlan.objects.get(id=training_plan_data['id'])

    #             for key, value in training_plan_data.items():
    #                 if key not in ['exercises', 'customer']:
    #                     setattr(training_plan, key, value)

    #             exercise_ids = [exercise['id'] for exercise in training_plan_data['exercises']]
    #             training_plan.exercises.set(Exercise.objects.filter(pk__in=exercise_ids))
    #             cus_profile = CustomerProfile.objects.get(id=training_plan_data['customer']['id'])
    #             training_plan.customer = cus_profile

    #             training_plan.save()

    #         except TrainingPlan.DoesNotExist:
    #             return Response({'message': 'Training plan not found!'}, status=status.HTTP_404_NOT_FOUND)
    #     else:
    #         return Response({"error": "No training plan data were provided!"}, status=status.HTTP_400_BAD_REQUEST)
        

    #     workout_schedule = WorkoutSchedule.objects.create(**serializer.validated_data, training_plan=training_plan)
    #     workout_schedule_serializer = WorkoutScheduleSerializer(workout_schedule)

    #     return Response(workout_schedule_serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], url_path='create-new', detail=False, permission_classes=[IsCoach | IsCustomer | IsAdmin],
        renderer_classes=[renderers.JSONRenderer])
    def create_new(self, request, *args, **kwargs):
        try:
            repeat_days = int(request.data.get('repeat_days', 0))  # Số ngày lặp lại
            print(repeat_days)
            start_time_str = request.data.get('start_time')
            end_time_str = request.data.get('end_time')

            start_time = parse_datetime(start_time_str)
            end_time = parse_datetime(end_time_str)

            if not start_time or not end_time:
                return Response({"error": "Invalid start_time or end_time"}, status=status.HTTP_400_BAD_REQUEST)

            customer_id = request.data.get('customer')
            coach_id = request.user.coach_profile.id

            tp_data = request.data.get('training_plan')
            training_plan_data = json.loads(tp_data) if tp_data else None

            if not training_plan_data:
                return Response({"error": "No training plan data provided"}, status=status.HTTP_400_BAD_REQUEST)

            # Lấy training plan
            try:
                training_plan = TrainingPlan.objects.get(id=training_plan_data['id'])

                for key, value in training_plan_data.items():
                    if key not in ['exercises', 'customer']:
                        setattr(training_plan, key, value)

                exercise_ids = [exercise['id'] for exercise in training_plan_data['exercises']]
                training_plan.exercises.set(Exercise.objects.filter(pk__in=exercise_ids))

                cus_profile = CustomerProfile.objects.get(id=training_plan_data['customer']['id'])
                training_plan.customer = cus_profile

                training_plan.save()

            except TrainingPlan.DoesNotExist:
                return Response({'message': 'Training plan not found!'}, status=status.HTTP_404_NOT_FOUND)

            created_schedules = []

            for i in range(repeat_days + 1):  # +1 để bao gồm cả ngày hiện tại
                new_start = start_time + timedelta(days=i)
                new_end = end_time + timedelta(days=i)

                schedule = WorkoutSchedule.objects.create(
                    start_time=new_start,
                    end_time=new_end,
                    customer_id=customer_id,
                    coach_id=coach_id,
                    training_plan=training_plan
                )
                print(schedule.start_time)
                print(schedule.end_time)
                created_schedules.append(schedule)

            serializer = WorkoutScheduleSerializer(created_schedules, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], url_path='edit-multiple', detail=False, permission_classes=[IsCoach | IsCustomer | IsAdmin], 
        renderer_classes=[renderers.JSONRenderer]) 
    def edit_multiple(self, request):
        ids = request.data.get('ids', [])
        completed = request.data.get('completed', None)

        if not ids or not isinstance(ids, list):
            return Response(
                {"error": "Invalid id list."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        try:
            schedules = WorkoutSchedule.objects.filter(id__in=ids)

            if not schedules.exists():
                return Response(
                    {"error": "No workout schedule(s) found with given id(s)."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            if completed is not None:
                schedules.update(completed=completed)

            serializer = self.get_serializer(schedules, many=True)

            return Response({"message": "Update schedule(s) successfully!", "data": serializer.data}, status=status.HTTP_200_OK,)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR,)
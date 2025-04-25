from django.db import models
from .training_plan import TrainingPlan


class WorkoutSchedule(models.Model):
    customer = models.ForeignKey('user_profile.CustomerProfile', related_name='customer_schedules', on_delete=models.CASCADE, null=True, blank=True, unique=False)
    coach = models.ForeignKey('user_profile.CoachProfile', related_name='coach_schedules', on_delete=models.CASCADE, null=True, blank=True, unique=False)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    training_plan = models.ForeignKey(TrainingPlan, on_delete=models.SET_NULL, null=True, blank=True, unique=False)

    attendance = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    class Meta:
        db_table = 'workout_schedule'

    

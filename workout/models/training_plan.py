from django.db import models
from .exercise import Exercise


class TrainingPlan(models.Model):
    customer = models.ForeignKey('user_profile.CustomerProfile', related_name='customer_training_plans', on_delete=models.CASCADE, null=True, blank=True)
    exercises = models.ManyToManyField(Exercise, related_name='exercise')
    estimated_duration = models.IntegerField(default=0)
    overview = models.TextField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'training_plan'

    

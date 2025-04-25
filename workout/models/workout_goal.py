from django.db import models


class WorkoutGoal(models.Model):
    general = models.CharField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    body_fat = models.FloatField(null=True, blank=True)
    muscle_mass = models.FloatField(null=True, blank=True)
    extra_data = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'workout_goal'



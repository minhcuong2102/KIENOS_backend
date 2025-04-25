from django.db import models
from user.models.user import User
from django.utils import timezone  


class CoachProfile(models.Model):
    coach = models.OneToOneField(User, on_delete=models.CASCADE, related_name='coach_profile')
    
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    gender = models.IntegerField()
    birthday = models.DateField()
    
    height = models.FloatField()
    weight = models.FloatField()
    start_date = models.DateField(default=timezone.now)
    experiences = models.TextField(null=True, blank=True)
    
    extra_data = models.JSONField(null=True, blank=True)

   
    class Meta:
        db_table = 'coach_profile'


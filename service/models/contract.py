from django.db import models
from datetime import timedelta
from .service import PTService, NonPTService
from user_profile.models.coach_profile import CoachProfile
from user_profile.models.customer_profile import CustomerProfile

class Contract(models.Model):
    ptservice = models.ForeignKey(PTService, on_delete=models.CASCADE, null=True, blank=True)
    nonptservice = models.ForeignKey(NonPTService, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    expire_date = models.DateField(null=True, blank=True)
    coach = models.ForeignKey(CoachProfile, related_name='coach_contracts', on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(CustomerProfile, related_name='customer_contracts', on_delete=models.CASCADE, null=True, blank=True)
    is_purchased = models.BooleanField(default=False)
    used_sessions = models.IntegerField(default=0)
    number_of_session = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        db_table = 'contract'
    




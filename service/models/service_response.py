from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from user_profile.models.coach_profile import CoachProfile
from user_profile.models.customer_profile import CustomerProfile
from django.utils import timezone


class ServiceResponse(models.Model):
    customer = models.ForeignKey(CustomerProfile, related_name="responses", on_delete=models.CASCADE)
    coach = models.ForeignKey(CoachProfile, related_name="ratings", on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField()
    score = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    responded = models.BooleanField(default=False)
    create_date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'service_response'


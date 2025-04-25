from django.contrib import admin
from .models.coach_profile import CoachProfile
from .models.customer_profile import CustomerProfile


admin.register(CustomerProfile)
admin.register(CoachProfile)
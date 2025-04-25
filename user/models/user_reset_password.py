from django.db import models
from .user import User

class UserResetPassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=256, null=True, blank=True)
    phone = models.CharField(max_length=256, null=True, blank=True)
    confirmed = models.BooleanField(default=False)
    expired_time = models.DateTimeField()
    last_modified_date = models.DateTimeField(auto_now=True)
    code = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        db_table = 'user_reset_password'


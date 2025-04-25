from django.db import models
from user.models import User
from .notification import Notification
from django.utils import timezone  


class NotificationUser(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications", null=True, blank=True)
    roles = models.CharField(max_length=255, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    create_date = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'notification_user'

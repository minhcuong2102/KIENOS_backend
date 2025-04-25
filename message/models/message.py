from django.db import models
from user.models.user import User


class Message(models.Model):
    content = models.TextField()
    sent_at = models.DateTimeField()
    coach_id = models.ForeignKey(User, related_name='coach_messages', on_delete=models.CASCADE)
    customer_id = models.ForeignKey(User, related_name='customer_messages', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    is_ai = models.BooleanField(default=False)
    extra_data = models.JSONField()
    
    class Meta:
        db_table = 'message'

    

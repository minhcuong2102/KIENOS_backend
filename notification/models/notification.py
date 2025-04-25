from django.db import models


class Notification(models.Model):
    message = models.TextField()
    params = models.JSONField(null=True, blank=True)
    create_url = models.TextField(null=True, blank=True)
    extra_data = models.JSONField(null=True, blank=True)
    
    class Meta:
        db_table = 'notification'




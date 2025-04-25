from django.db import models
from ..models.category import Category

class Exercise(models.Model):
    name = models.CharField(max_length=255)
    duration = models.IntegerField()
    repetitions = models.CharField(max_length=255)
    image_url = models.ImageField(upload_to='media/exercises/', blank=True, null=True)
    rest_period = models.IntegerField(default=45)
    categories = models.ManyToManyField(Category)
    embedded_video_url = models.TextField(null=True, blank=True, default="")

    class Meta:
        db_table = 'exercise'


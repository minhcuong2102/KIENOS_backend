from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Exercise
import boto3
from django.conf import settings

@receiver(post_delete, sender=Exercise)
def delete_exercise_image_from_s3(sender, instance, **kwargs):
    if instance.image_url:
        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        s3_key = instance.image_url.name 
        s3.delete_object(Bucket=bucket_name, Key=s3_key)
        print('DELETED IMAGE')

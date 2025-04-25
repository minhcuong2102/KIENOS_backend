from django.contrib import admin
from notification.models.notification import Notification
from notification.models.notification_user import NotificationUser


admin.register(Notification)
admin.register(NotificationUser)
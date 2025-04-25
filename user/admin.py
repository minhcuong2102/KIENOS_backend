from django.contrib import admin
from .models.user import User
from .models.user_reset_password import UserResetPassword
from .models.role import Role


admin.register(User)
admin.register(UserResetPassword)
admin.register(Role)
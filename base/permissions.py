from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role.name == 'admin'

class IsSale(BasePermission):
    def has_permission(self, request, view):
        return request.user.role.name == 'sale'

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.role.name == 'customer'

class IsCoach(BasePermission):
    def has_permission(self, request, view):
        return request.user.role.name == 'coach'

class IsCoachOrCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.role.name == 'coach' or request.user.role.name == 'customer'
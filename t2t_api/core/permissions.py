from rest_framework.permissions import BasePermission

class IsUser(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.user_type == 'user'

class IsStaff(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.user_type == 'staff'
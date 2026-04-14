from rest_framework.permissions import BasePermission

class RolePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.role == "admin":
            return True

        if user.role == "manager":
            return obj.created_by == user

        if user.role == "user":
            return obj.id == user.id

        return False
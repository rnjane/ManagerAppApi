from rest_framework import permissions

class AllowOwnerOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.time_budget_owner == request.user
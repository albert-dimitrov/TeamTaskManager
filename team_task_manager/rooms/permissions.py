from rest_framework import permissions

class IsLeaderOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user in obj.members.all() or request.user == obj.leaders or request.user.is_staff

        return request.user == obj.leaders or request.user.is_staff
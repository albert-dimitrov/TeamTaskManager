from rest_framework import permissions


class IsLeaderOrAdminOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user in obj.room.members.all() or request.user.is_staff

        return request.user == obj.room.leaders or request.user.is_staff


class IsAssignedUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (
            request.user == obj.assigned_to
            or request.user == obj.room.leaders
            or request.user.is_staff
        )

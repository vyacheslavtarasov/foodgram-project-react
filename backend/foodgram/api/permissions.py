from rest_framework.permissions import BasePermission


class Browse4AllEdit4Author(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True

        return obj.author == request.user

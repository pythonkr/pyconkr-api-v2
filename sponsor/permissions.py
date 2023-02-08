from rest_framework import permissions

from sponsor.models import Sponsor


class IsOwnerOrReadOnly(permissions.BasePermission):
    # https://stackoverflow.com/questions/72691826/djnago-rest-framework-how-to-allow-only-update-user-own-content-only
    def has_object_permission(self, request, view, obj: Sponsor):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.manager_id == request.user or obj.creator == request.user


class OwnerOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Sponsor):
        return obj.manager_id == request.user or obj.creator == request.user

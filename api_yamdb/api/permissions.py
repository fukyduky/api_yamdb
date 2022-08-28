from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `author` attribute.
    """
    message = 'Изменение чужого контента запрещено!'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user


class AdminOrReadOnly(permissions.BasePermission):
    # Право для всех на чтение
    # Право админа на создание категории, жанра, произведения
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin()
                or request.method in permissions.SAFE_METHODS)


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_admin
                     or request.user.is_superuser))

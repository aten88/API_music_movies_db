from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    '''Кастомный пермишен Админа.'''
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and (request.user.is_admin or request.user.is_superuser)))


class IsReviewOwnerOrReadOnly(permissions.BasePermission):
    '''Кастомный пермишен отзыва.'''
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                or request.method in permissions.SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or (request.user.is_admin or request.user.is_moderator))


class IsAdmin(permissions.BasePermission):
    '''Кастомный пермишен Админа.'''
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser)

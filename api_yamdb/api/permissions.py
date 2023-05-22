from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    '''Кастомный пермишен Админа.'''
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_staff or request.user.role == 'admin'


class IsReviewOwnerOrReadOnly(permissions.BasePermission):
    '''Кастомный пермишен отзыва.'''
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.role in ('admin', 'moderator'))


class IsAdmin(permissions.BasePermission):
    '''Кастомный пермишен Админа.'''
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin() or request.user.is_superuser)

from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """
    Предоставляет доступ только пользователям из группы 'moderators'.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.groups.filter(name="moderators").exists()
        )

    def has_object_permission(self, request, view, obj):
        # Модераторы могут просматривать и редактировать (GET, PUT, PATCH),
        # но не создавать и удалять (POST, DELETE) — контролируется в get_permissions контроллеров
        if request.method in permissions.SAFE_METHODS or request.method in [
            "PUT",
            "PATCH",
        ]:
            return True
        return False


class IsOwner(permissions.BasePermission):
    """
    Позволяет работать с объектом только его владельцу.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешаем безопасные методы всем (если нужно)
        if request.method in permissions.SAFE_METHODS:
            return True
        # Проверяем, что у объекта есть поле owner и оно совпадает с пользователем
        return hasattr(obj, "owner") and obj.owner == request.user

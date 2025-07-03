from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOfCourseOrModerator(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешаем читать всем
        if request.method in SAFE_METHODS:
            return True
        # Для изменений — владелец урока или модератор
        return obj.owner == request.user or request.user.is_staff

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not (request.user and request.user.is_authenticated):
            return False

        # Для создания урока проверяем, что пользователь владеет курсом
        if request.method == 'POST':
            course_id = request.data.get('course')
            if not course_id:
                return False
            # Проверяем, что курс принадлежит пользователю или он модератор
            from educations.models import Course
            try:
                course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                return False
            return course.owner == request.user or request.user.is_staff

        return True

class OwnerOrModeratorQuerysetMixin:
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()
        user = self.request.user
        if not user.is_authenticated:
            return self.queryset.none()

        if user.is_superuser or user.groups.filter(name="moderators").exists():
            return self.queryset.all()
        return self.queryset.filter(owner=user)

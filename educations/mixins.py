class OwnerOrModeratorQuerysetMixin:
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name="moderators").exists():
            return self.queryset.all()
        return self.queryset.filter(owner=user)

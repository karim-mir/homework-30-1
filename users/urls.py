from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UserRegisterAPIView, UserViewSet

router = DefaultRouter()
router.register(r"", UserViewSet)

urlpatterns = [
    path("register/", UserRegisterAPIView.as_view(), name="user-register"),
    path("", include(router.urls)),
]

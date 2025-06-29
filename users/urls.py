from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, UserRegisterAPIView

router = DefaultRouter()
router.register(r'', UserViewSet)

urlpatterns = [
    path('register/', UserRegisterAPIView.as_view(), name='user-register'),
    path('', include(router.urls)),
]

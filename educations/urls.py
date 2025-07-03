from django.urls import include, path
from rest_framework.routers import DefaultRouter

from educations.views import (CourseViewSet, LessonListCreateAPIView,
                              LessonRetrieveUpdateDestroyAPIView,
                              PaymentListAPIView, SubscriptionAPIView)

router = DefaultRouter()
router.register(r"courses", CourseViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("lessons/", LessonListCreateAPIView.as_view(), name="lesson-list-create"),
    path(
        "lessons/<int:pk>/",
        LessonRetrieveUpdateDestroyAPIView.as_view(),
        name="lesson-detail",
    ),
    path("payments/", PaymentListAPIView.as_view(), name="payment-list"),
    path("subscriptions/", SubscriptionAPIView.as_view(), name="subscriptions"),
]

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import filters, generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from educations.mixins import OwnerOrModeratorQuerysetMixin
from educations.models import Course, Lesson, Payment, Subscription
from educations.serializers import (CourseSerializer, LessonSerializer,
                                    PaymentSerializer)
from users.permissions import IsModerator, IsOwner


class CourseViewSet(OwnerOrModeratorQuerysetMixin, viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListCreateAPIView(
    OwnerOrModeratorQuerysetMixin, generics.ListCreateAPIView
):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDestroyAPIView(
    OwnerOrModeratorQuerysetMixin, generics.RetrieveUpdateDestroyAPIView
):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("paid_course", "paid_lesson", "payment_method")
    ordering_fields = ["payment_date"]
    ordering = ["-payment_date"]

    def get_queryset(self):
        user = self.request.user
        # Показываем платежи только текущего пользователя
        return Payment.objects.filter(user=user)


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")

        if not course_id:
            return Response({"error": "course_id не указан"}, status=400)

        course = get_object_or_404(Course, id=course_id)
        subs_qs = Subscription.objects.filter(user=user, course=course)

        if subs_qs.exists():
            subs_qs.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "Подписка создана"

        return Response({"message": message})

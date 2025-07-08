from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from educations.models import Course
from payments.models import Payment
from users.models import User


class PaymentAPITests(APITestCase):
    def setUp(self):
        # Создаем пользователя и курс
        self.user = User.objects.create_user(
            email="user@example.com", password="pass1234"
        )
        self.course = Course.objects.create(
            course_name="Test Course", description="Test description", owner=self.user
        )
        self.create_url = reverse("payment-create")
        self.status_url = reverse("payment-status")

    def test_create_payment_success(self):
        self.client.force_authenticate(user=self.user)
        data = {"paid_course": self.course.id, "amount": 10.0}  # сумма в долларах
        response = self.client.post(self.create_url, data, format="json")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("checkout_url", response.data)
        self.assertIn("payment_id", response.data)
        self.assertTrue(Payment.objects.filter(id=response.data["payment_id"]).exists())

    def test_create_payment_unauthenticated(self):
        data = {"paid_course": self.course.id, "amount": 10.0}
        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_payment_status_missing_session_id(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.status_url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("session_id не указан", response.data.get("error", ""))

    def test_payment_status_invalid_session_id(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.status_url, {"session_id": "invalid_session"})
        print(response.data)
        # Ожидаем ошибку от Stripe, например 400 или 404
        self.assertIn(
            response.status_code,
            [status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND],
        )
        self.assertIn("error", response.data)

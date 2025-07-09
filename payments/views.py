import stripe
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from payments.models import Payment
from payments.serializers import PaymentSerializer
from payments.services import (create_stripe_checkout_session,
                               create_stripe_price, create_stripe_product)


class PaymentAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        """Получаем данные платежа из serializer.validated_data"""
        course = serializer.validated_data.get("paid_course")
        amount = serializer.validated_data.get("amount") * 100

        product_name = course.course_name if course else "Course Payment"
        product_description = getattr(course, "description", "")

        product = create_stripe_product(
            name=product_name, description=product_description
        )
        price = create_stripe_price(product.id, amount=amount)

        course_id = course.id if course else None
        success_url = f"http://127.0.0.1:8000/educations/{course_id}/" if course_id else "https://127.0.0.1:8000/educations/"
        cancel_url = "https://yourdomain.com/educations/payment-cancelled/"
        session = create_stripe_checkout_session(
            price_id=price.id,
            success_url=success_url,
            cancel_url=cancel_url,
        )

        payment = serializer.save(
            amount=serializer.validated_data.get("amount"),
            session_id=session.id,
            link=session.url,
            user=self.request.user,
            paid_course=course,
        )

        self.response_data = {"payment_id": payment.id, "checkout_url": session.url}

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(self.response_data, status=status.HTTP_201_CREATED)


class PaymentStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        session_id = request.query_params.get("session_id")
        if not session_id:
            return Response(
                {"error": "session_id не указан"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            session = stripe.checkout.Session.retrieve(session_id)
        except stripe.error.StripeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {
                "id": session.id,
                "payment_status": session.payment_status,
                "amount_total": session.amount_total,
                "currency": session.currency,
                "customer_details": session.customer_details,
                "payment_intent": session.payment_intent,
            }
        )

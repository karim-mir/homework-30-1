from django.urls import path

from payments.views import PaymentAPIView, PaymentStatusAPIView

urlpatterns = [
    path("create/", PaymentAPIView.as_view(), name="payment-create"),
    path("status/", PaymentStatusAPIView.as_view(), name="payment-status"),
]

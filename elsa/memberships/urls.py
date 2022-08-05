from django.urls import path

from rest_framework import routers

from . import views
from . import viewsets


router = routers.SimpleRouter()
router.register(
    "memberships", viewsets.MembershipViewSet, basename="memberships"
)
router.register("payments", viewsets.PaymentViewSet, basename="payments")

urlpatterns = [
    path(
        "memberships/buy/",
        views.BuyMembershipView.as_view(),
        name="membership_buy",
    ),
    path(
        "memberships/buy/paypal/",
        views.BuyMembershipViaPaypalView.as_view(),
        name="membership_buy_paypal",
    ),
    path(
        "memberships/payu/response/",
        views.PayUResponseView.as_view(),
        name="payu_response",
    ),
    path(
        "memberships/payu/confirm/",
        views.PayUConfirmationView.as_view(),
        name="payu_confirm",
    ),
]
urlpatterns += router.urls

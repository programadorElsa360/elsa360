import logging

from datetime import datetime, timezone, timedelta
from decimal import Decimal
from uuid import uuid4

from configuration.settings.config_utils import get_env_variable

from dateutil.relativedelta import relativedelta

from django.shortcuts import get_object_or_404, render

from elsa.users.models import CustomUser

from knox.auth import TokenAuthentication

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Coupon, CouponToUser, Membership, Payment
from .serializers import PaymentSerializer
from .utils import generate_payu_signature

PAYU_API_KEY = get_env_variable("PAYU_API_KEY")


# Create your views here.
class BuyMembershipView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data

        membership_tier = data.get("membership")
        currency = data.get("currency", Payment.AllowedCoins.COP.value)

        membership = get_object_or_404(Membership, tier=membership_tier)
        merchant_id = get_env_variable("PAYU_MERCHANT_ID")
        reference_code = str(uuid4()).replace("-", "")
        amount = "{:.2f}".format(membership.price)
        api_url = get_env_variable("API_URL")

        signature_string = (
            f"{PAYU_API_KEY}~{merchant_id}~"
            + f"{reference_code}~{amount}~{currency}"
        )

        # Apply coupon if possible.
        discount = Decimal(0.00)
        coupon_name = data.get("coupon", "")
        coupon = None
        # Check coupon code exists.
        if coupon_name:
            try:
                coupon = Coupon.objects.get(name=coupon_name)
            except Coupon.DoesNotExist:
                return Response(
                    "The provided coupon does not exist.",
                    status=status.HTTP_200_OK,
                )
            # Check coupon code is still valid for the current date.
            current_date = datetime.fromisoformat("2022-07-15").astimezone(
                timezone.utc
            )  # datetime.now(timezone.utc)
            if not coupon.is_valid_date(current_date):
                return Response(
                    "The provided coupon has expired or is not valid yet.",
                    status=status.HTTP_200_OK,
                )
            # Validate the user hasn't used the same code previously.
            if user.used_coupons.filter(pk=coupon.pk):
                return Response(
                    "The provided coupon has already been redeemed.",
                    status=status.HTTP_200_OK,
                )

        serializer_data = {
            "user": request.user.pk,
            "membership_purchased": membership.pk,
            "reference_code": reference_code,
            "amount": amount,
            "currency": currency,
        }
        serializer = PaymentSerializer(data=serializer_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Payment data is fine and all coupon checks pass so
        # create an entry in the used coupons table for this user.
        if coupon:
            CouponToUser.objects.create(user=user, coupon=coupon)
            user.used_coupons.add(coupon.pk)

            # Apply discount.
            discount = membership.price * Decimal(coupon.discount)

        amount = "{:.2f}".format(membership.price - discount)
        tax = "{:.2f}".format(membership.price * Decimal(0.19))

        return render(
            request,
            "payu_purchase_form.html",
            {
                "pay_webcheckout_url": get_env_variable(
                    "PAYU_WEBCHECKOUT_URL"
                ),
                "merchant_id": merchant_id,
                "account_id": get_env_variable("PAYU_ACCOUNT_ID"),
                "description": "ELSA Membership payment",
                "reference_code": reference_code,
                "amount": amount,
                "tax": tax,
                "tax_return_base": 0,
                "currency": currency,
                "signature": generate_payu_signature(signature_string),
                "test": int(bool(get_env_variable("PAYU_TEST_MODE"))),
                "buyer_email": request.user.email,
                "response_url": f"{api_url}/memberships/payu/response/",
                "confirmation_url": f"{api_url}/memberships/payu/confirm/",
            },
        )


class PayUResponseView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        logging.info("PayU Response endpoint triggered.")
        data = request.query_params

        # Transaction details.
        merchant_id = int(data.get("merchantId"))
        tx_state = int(data.get("transactionState"))
        reference_code = data.get("referenceCode")
        reference_pol = data.get("reference_pol")
        tx_signature = data.get("signature")
        TX_VALUE = float(data.get("TX_VALUE"))
        processing_date = data.get("processingDate")
        currency = data.get("currency")

        new_tx_value = round(TX_VALUE, 2)

        signature_string = (
            f"{PAYU_API_KEY}~{merchant_id}~{reference_code}~"
            + f"{new_tx_value}~{currency}~{tx_state}"
        )
        logging.debug(signature_string)
        generated_signature = generate_payu_signature(signature_string)

        if tx_signature != generated_signature:
            error_msg = "Error validating tx signature: Signatures don't match"
            logging.warning(error_msg)

            return Response(
                {"message": error_msg},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                "state": next(
                    member.label
                    for _, member in Payment.PaymentStatus.__members__.items()
                    if member.value == tx_state
                ),
                "reference_code": reference_code,
                "reference_pol": reference_pol,
                "amount": TX_VALUE,
                "currency": currency,
                "processing_date": processing_date,
            },
            status=status.HTTP_200_OK,
        )


class PayUConfirmationView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        logging.info("PayU Confirmation endpoint triggered.")
        data = request.data

        merchant_id = int(data.get("merchant_id"))
        state_pol = int(data.get("state_pol"))
        reference_sale = data.get("reference_sale")
        value = float(data.get("value"))
        currency = data.get("currency")
        signature = data.get("sign")

        value_str = str(value)
        if "." in value_str:
            base, decimals = value_str.split(".")
            if len(decimals) == 2 and decimals[-1] == "0":
                new_tx_value = round(value, 1)
            else:
                new_tx_value = value
        else:
            new_tx_value = value

        signature_string = (
            f"{PAYU_API_KEY}~{merchant_id}~{reference_sale}~"
            + f"{new_tx_value}~{currency}~{state_pol}"
        )
        generated_signature = generate_payu_signature(signature_string)
        logging.info(signature_string)

        if signature != generated_signature:
            error_msg = "Error validating tx signature: Signatures don't match"
            logging.warning(error_msg)

            return Response(
                {"message": error_msg},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Update payment transaction in DB.
        payment = get_object_or_404(Payment, reference_code=reference_sale)
        payment.status = state_pol
        payment.save()
        payment.refresh_from_db()

        # Update user's training start date in DB.
        if payment.status == Payment.PaymentStatus.APPROVED:
            user = get_object_or_404(CustomUser, pk=payment.user.pk)
            membership = get_object_or_404(
                Membership, pk=payment.membership_purchased.pk
            )

            # Training starts next Monday after payment.
            today = datetime.today()
            months = membership.tier
            rel_timedelta = relativedelta(months=+months)

            training_start = today + timedelta(days=-today.weekday(), weeks=1)
            user.training_start = training_start
            user.training_end = training_start + rel_timedelta
            user.membership = membership
            user.save()

        return Response(status=status.HTTP_200_OK)


class BuyMembershipViaPaypalView(APIView):
    def post(self, request):
        data = request.data

        membership_tier = int(data.get("membership"))
        membership = get_object_or_404(Membership, tier=membership_tier)

        if membership.tier == 3:
            plan_id_variable = "PAYPAL_TRIMESTER_PLAN_ID"
        elif membership.tier == 6:
            plan_id_variable = "PAYPAL_SEMESTER_PLAN_ID"
        elif membership_tier == 12:
            plan_id_variable = "PAYPAL_YEARLY_PLAN_ID"

        paypal_client_id = get_env_variable("PAYPAL_CLIENT_ID")
        paypal_plan_id = get_env_variable(plan_id_variable)

        # TODO edit template to support rendering of multiple
        # payment buttons.
        return render(
            request,
            "paypal_pay_button.html",
            {"client_id": paypal_client_id, "plan_id": paypal_plan_id},
        )

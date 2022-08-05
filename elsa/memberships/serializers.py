from rest_framework import serializers

from .models import Membership, Payment, Coupon


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ["tier", "price"]


class PaymentSerializer(serializers.ModelSerializer):
    status_label = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = [
            "user",
            "status",
            "status_label",
            "reference_code",
            "membership_purchased",
            "amount",
            "currency",
        ]

    def get_status_label(self, obj):
        return obj.get_status_display()


class CouponSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        """Validate that the validity end date comes after the start date."""
        validity_start_date = attrs["valid_start_date"]
        validity_end_date = attrs["valid_end_date"]

        if validity_end_date < validity_start_date:
            raise serializers.ValidationError(
                "Validity end date cannot be earlier than start date"
            )

        return attrs

    class Meta:
        model = Coupon
        fields = ["name", "discount", "valid_start_date", "valid_end_date"]

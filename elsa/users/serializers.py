from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "pk",
            "is_staff",
            "username",
            "email",
            "is_email_verified",
            "age",
            "gender",
            "height",
            "weight",
            "weight_goal",
            "diet",
            "sports_level",
            "sports_goal",
            "weekly_training",
            "hourly_training",
            "body_type",
            "body_goal",
            "membership",
            "training_start",
            "training_end",
            "update_info",
        ]
        read_only_fields = [
            "pk",
            "is_staff",
            "is_email_verified",
            "update_info",
        ]


class RegisterUserSerializer(serializers.Serializer):
    user = UserSerializer()
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, data):
        if data.get("password") != data.get("confirm_password"):
            raise serializers.ValidationError(
                {"password_&_confirm_password": "Passwords do not match."}
            )
        # User model does not use the 'confirm_password' field.
        data.pop("confirm_password")

        return data

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        user.set_password(validated_data["password"])
        user.save()
        return user


class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"email": "An User with the specified email does not exist."}
            )

        return value

    class Meta:
        fields = ["email"]


class PerformPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    def validate(self, data):
        if data.get("password") != data.get("confirm_password"):
            raise serializers.ValidationError(
                {"password_&_confirm_password": "Passwords do not match."}
            )

        return data

    class Meta:
        fields = ["password", "confirm_password", "uidb64", "token"]

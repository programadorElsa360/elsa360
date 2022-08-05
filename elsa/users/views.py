from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from knox.views import LoginView as KnoxLoginView

from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    RequestPasswordResetSerializer,
    PerformPasswordResetSerializer,
)
from .utils import generate_token, send_password_reset_email

User = get_user_model()


# Create your views here.
class LoginView(KnoxLoginView):
    authentication_classes = [BasicAuthentication]


class VerifyUserView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uuid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uuid)
        except Exception:
            user = None

        if user and generate_token.check_token(user, token):
            user.is_email_verified = True
            user.save()
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = RequestPasswordResetSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        user = get_object_or_404(User, email=email)

        send_password_reset_email(user, request)

        return Response(status=status.HTTP_200_OK)


class ConfirmPasswordResetView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uuid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uuid)
        except Exception:
            user = None

        if user and PasswordResetTokenGenerator().check_token(user, token):
            return Response(status=status.HTTP_200_OK)

        return Response(
            {
                "message": "The password reset link either has "
                + "been used already or has expired"
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )


class PerformPasswordResetView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = PerformPasswordResetSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_password = serializer.validated_data["password"]
        uidb64 = serializer.validated_data["uidb64"]
        token = serializer.validated_data["token"]

        try:
            uuid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uuid)
        except Exception:
            user = None

        if user and PasswordResetTokenGenerator().check_token(user, token):
            user.set_password(new_password)
            user.save()

            return Response(status=status.HTTP_200_OK)

        return Response(
            {
                "message": "The password reset link either has "
                + "been used already or has expired"
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

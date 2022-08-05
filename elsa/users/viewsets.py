from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from knox.auth import TokenAuthentication

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .serializers import RegisterUserSerializer, UserSerializer

from .utils import send_confirmation_email


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User model CRUD."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of
        permissions that this view requires.
        """
        if self.action == "destroy":
            permission_classes = [IsAdminUser]
        elif self.action in ["register", "resend_confirmation"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.request is None:
            return User.objects.none()

        if self.request.user.is_staff:
            return User.objects.all()
        else:
            return User.objects.filter(pk=self.request.user.pk)

    @action(
        detail=False,
        methods=["post"],
        serializer_class=RegisterUserSerializer,
        permission_classes=[AllowAny],
    )
    def register(self, request):
        data = request.data
        register_user_serializer = self.serializer_class(data=data)

        register_user_serializer.is_valid(raise_exception=True)
        user = register_user_serializer.save()

        # Send confirmation email to the user so
        # they can verify their account and login.
        send_confirmation_email(user, request)

        return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"], permission_classes=[AllowAny])
    def resend_confirmation(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        send_confirmation_email(user, request)

        return Response(
            {"message": "Confirmation email re-sent."},
            status=status.HTTP_200_OK,
        )

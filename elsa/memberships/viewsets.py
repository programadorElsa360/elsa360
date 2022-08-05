from knox.auth import TokenAuthentication

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Membership, Payment
from .serializers import MembershipSerializer, PaymentSerializer


class MembershipViewSet(ModelViewSet):
    """ViewSet for Membership model CRUD."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    filterset_fields = ["tier"]


class PaymentViewSet(ReadOnlyModelViewSet):
    """ViewSet for read-only Payment endpoints."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

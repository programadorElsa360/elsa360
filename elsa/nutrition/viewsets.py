from knox.auth import TokenAuthentication

from rest_framework.viewsets import ModelViewSet

from .models import Food
from .serializers import FoodSerializer


class FoodViewSet(ModelViewSet):
    """ViewSet for Food model CRUD."""

    authentication_classes = [TokenAuthentication]
    serializer_class = FoodSerializer
    queryset = Food.objects.all()
    filterset_fields = ["food_group__group"]

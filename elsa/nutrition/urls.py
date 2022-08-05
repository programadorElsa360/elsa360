from django.urls import path

from rest_framework import routers

from . import views
from . import viewsets

router = routers.SimpleRouter()

router.register("foods", viewsets.FoodViewSet, basename="foods")

urlpatterns = [
    path(
        "nutrition/daily/",
        views.DailyNutritionalPlanView.as_view(),
        name="nutrition_daily",
    ),
    path(
        "nutrition/intake/",
        views.DailyNutritionalBillCalculationsView.as_view(),
        name="nutrition_intake",
    ),
]

urlpatterns += router.urls

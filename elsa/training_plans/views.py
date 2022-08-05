import logging

from knox.auth import TokenAuthentication

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from elsa.commons.authentication import IsAdminOrHasMembership

from .models import CyclingPlan, PhysicPlan
from .api import build_complete_plan, get_daily_plans


# Create your views here.
class CompleteTrainingPlanView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrHasMembership]

    def get(self, request):
        logging.info("Get CompleteTrainingPlan endpoint triggered.")
        user = request.user
        membership_length = user.membership.tier

        cycling_plans_qs = CyclingPlan.objects.filter(
            variables__gender=user.gender,
            variables__sports_goal=user.sports_goal,
            variables__sports_level=user.sports_level,
        ).order_by("week", "day")
        physic_plans_qs = PhysicPlan.objects.filter(
            variables__gender=user.gender,
            variables__sports_goal=user.sports_goal,
            variables__sports_level=user.sports_level,
        ).order_by("week", "day")

        cycling_training_base = cycling_plans_qs.values()
        physic_training_base = physic_plans_qs.values()

        # Group all this data by week.
        cycling_weeks = build_complete_plan(
            user, cycling_training_base, membership_length
        )
        physic_weeks = build_complete_plan(
            user, physic_training_base, membership_length
        )

        return Response(
            data={"cycling": cycling_weeks, "physic": physic_weeks},
            status=status.HTTP_200_OK,
        )


class DailyTrainingPlansView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrHasMembership]

    def get(self, request):
        user = request.user
        cycling_plans, physic_plans = get_daily_plans(
            user,
            user.current_training_day["relative"],
            user.current_training_week["relative"],
        )

        return Response(
            data={"cycling": cycling_plans, "physic": physic_plans},
            status=status.HTTP_200_OK,
        )

import logging

from django.contrib.auth import get_user_model
from django.contrib.postgres.aggregates import ArrayAgg

from elsa.nutrition.api import get_total_energy_expenditure

from .models import CyclingPlan, PhysicPlan, QuestionsToPlan
from .serializers import CyclingPlanSerializer, PhysicPlanSerializer

User = get_user_model()


def build_complete_plan(user, base_plan, membership_length):
    complete_plan = {}
    calendar_length = 0
    while calendar_length < membership_length * 4:
        if not base_plan.exists():
            logging.warning(
                "No base plan entries found, please seed the database."
            )
            break

        for entry in base_plan:
            tee, weight_goal_conclusion = get_total_energy_expenditure(
                user, entry["day"], entry["week"]
            )
            entry["total_energy_expenditure"] = (
                tee,
                weight_goal_conclusion.value,
            )

            new_key = entry["week"] + calendar_length
            if new_key not in complete_plan.keys():
                complete_plan[new_key] = [entry]
            else:
                complete_plan[new_key].append(entry)

        calendar_length = len(complete_plan.keys())

    return complete_plan


def get_daily_plans(user: User, relative_day, relative_week):
    cycling_plans_ids = QuestionsToPlan.objects.filter(
        gender=user.gender,
        sports_goal=user.sports_goal,
        sports_level=user.sports_level,
        cyclingplan__day=relative_day,
        cyclingplan__week=relative_week,
    ).aggregate(cycling_plans_ids=ArrayAgg("cyclingplan", distinct=True))

    physic_plans_ids = QuestionsToPlan.objects.filter(
        gender=user.gender,
        sports_goal=user.sports_goal,
        sports_level=user.sports_level,
        physicplan__day=relative_day,
        physicplan__week=relative_week,
    ).aggregate(physic_plans_ids=ArrayAgg("physicplan", distinct=True))

    cycling_plans_qs = CyclingPlan.objects.filter(
        pk__in=cycling_plans_ids["cycling_plans_ids"]
    )

    physic_plans_qs = PhysicPlan.objects.filter(
        pk__in=physic_plans_ids["physic_plans_ids"]
    )

    c_serializer = CyclingPlanSerializer(cycling_plans_qs, many=True)
    p_serializer = PhysicPlanSerializer(physic_plans_qs, many=True)

    return c_serializer.data, p_serializer.data

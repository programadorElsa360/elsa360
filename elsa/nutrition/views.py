from django.db.models import Sum
from django.core.exceptions import ValidationError

from knox.auth import TokenAuthentication

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from elsa.commons.authentication import IsAdminOrHasMembership
from elsa.commons.enums import CalorieIntakeTiers

from .models import Food, MealSummary
from .serializers import MealSummarySerializer
from .api import (
    WeightGoals,
    get_total_energy_expenditure,
)


# Create your views here.
class DailyNutritionalPlanView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrHasMembership]

    def get(self, request):
        user = request.user

        user_age = user.age
        user_height = user.height
        user_weight = user.weight
        user_weight_goal = user.weight_goal

        if any(
            [
                user_age is None,
                user_height is None,
                user_weight is None,
                user_weight_goal is None,
            ]
        ):
            return Response(
                {
                    "message": "Please make sure you've "
                    + "set valid values for your 'age', 'height',"
                    + " 'weight and 'weight_goal'."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        user_heigth_squared = user.height_in_meters**2

        liquid_requirement = round((35 * user_weight) / 1000, 2)
        body_mass_index = user_weight / (user_heigth_squared)
        BODY_MASS_INDEX_VALUES = {
            18.4: "Underweight",
            24.9: "Normal",
            29.9: "Overweight",
            34.9: "Obesity type 1",
            39.9: "Obesity type 2",
        }
        healthy_weight_ranges = {
            "lower limit": round(19.5 * (user_heigth_squared), 2),
            "ideal weight": round(21.7 * (user_heigth_squared), 2),
            "upper limit": round(23.9 * (user_heigth_squared), 2),
        }
        body_mass_index_goal = user_weight_goal / (user_heigth_squared)

        bmi_status = "Morbid Obesity"
        bmi_goal_status = "Morbid Obesity"
        for key, value in BODY_MASS_INDEX_VALUES.items():
            if body_mass_index < key:
                bmi_status = value
                break

        for key, value in BODY_MASS_INDEX_VALUES.items():
            if body_mass_index_goal < key:
                bmi_goal_status = value
                break

        if body_mass_index_goal < 19.5:
            return Response(
                {
                    "health_warning": "Your Weight Goal is too low and is "
                    + "Unhealthy, please add some Kg for a healthy weight"
                },
                status=status.HTTP_200_OK,
            )
        elif body_mass_index_goal > 23.9:
            return Response(
                {
                    "health_warning": "Your Weight Goal is too high and is "
                    + "Unhealthy, please remove some Kg for a healthy weight"
                },
                status=status.HTTP_200_OK,
            )

        relative_day = user.current_training_day["relative"]
        relative_week = user.current_training_week["relative"]

        (
            total_energy_expenditure,
            weight_goal_conclusion,
        ) = get_total_energy_expenditure(user, relative_day, relative_week)

        TEE_PERCENTAGES_PER_GOAL = {
            WeightGoals.GAIN: {
                "carbohydrates": 0.53,
                "protein": 0.25,
                "fats": 0.22,
            },
            WeightGoals.LOSE: {
                "carbohydrates": 0.48,
                "protein": 0.30,
                "fats": 0.22,
            },
            WeightGoals.MAINTAIN: {
                "carbohydrates": 0.54,
                "protein": 0.16,
                "fats": 0.30,
            },
        }

        daily_carbohydrates = (
            total_energy_expenditure
            * TEE_PERCENTAGES_PER_GOAL[weight_goal_conclusion]["carbohydrates"]
        )
        daily_protein = (
            total_energy_expenditure
            * TEE_PERCENTAGES_PER_GOAL[weight_goal_conclusion]["protein"]
        )
        daily_fats = (
            total_energy_expenditure
            * TEE_PERCENTAGES_PER_GOAL[weight_goal_conclusion]["fats"]
        )

        daily_carbohydrates_grams = daily_carbohydrates / 4
        daily_protein_grams = daily_protein / 4
        daily_fats_grams = daily_fats / 9

        MEALS_DISTRIBUTION_PER_GOAL = {
            WeightGoals.GAIN: {
                MealSummary.MealTimes.BREAKFAST: 0.20,
                MealSummary.MealTimes.SNACK_1: 0.15,
                MealSummary.MealTimes.LUNCH: 0.20,
                MealSummary.MealTimes.SNACK_2: 0.15,
                MealSummary.MealTimes.DINNER: 0.20,
                MealSummary.MealTimes.NIGHT_SNACK: 0.10,
            },
            WeightGoals.LOSE: {
                MealSummary.MealTimes.BREAKFAST: 0.22,
                MealSummary.MealTimes.SNACK_1: 0.15,
                MealSummary.MealTimes.LUNCH: 0.28,
                MealSummary.MealTimes.SNACK_2: 0.15,
                MealSummary.MealTimes.DINNER: 0.20,
                MealSummary.MealTimes.NIGHT_SNACK: 0,
            },
            WeightGoals.MAINTAIN: {
                MealSummary.MealTimes.BREAKFAST: 0.25,
                MealSummary.MealTimes.SNACK_1: 0.15,
                MealSummary.MealTimes.LUNCH: 0.35,
                MealSummary.MealTimes.SNACK_2: 0,
                MealSummary.MealTimes.DINNER: 0.25,
                MealSummary.MealTimes.NIGHT_SNACK: 0,
            },
        }

        meal_data = {}
        for meal in MealSummary.MealTimes:
            meal_percentage = MEALS_DISTRIBUTION_PER_GOAL[
                weight_goal_conclusion
            ][meal]
            meal_kcal = total_energy_expenditure * meal_percentage
            meal_carbohydrates = daily_carbohydrates * meal_percentage
            meal_protein = daily_protein * meal_percentage
            meal_fats = daily_fats * meal_percentage
            meal_carbohydrates_grams = (
                daily_carbohydrates_grams * meal_percentage
            )
            meal_protein_grams = daily_protein_grams * meal_percentage
            meal_fats_grams = daily_fats_grams * meal_percentage

            meal_data[meal.name] = {
                "total_kcal": round(meal_kcal, 2),
                "carbohydrates": round(meal_carbohydrates, 2),
                "carbohydrates_grams": round(meal_carbohydrates_grams, 2),
                "protein": round(meal_protein, 2),
                "protein_grams": round(meal_protein_grams, 2),
                "fats": round(meal_fats, 2),
                "fats_grams": round(meal_fats_grams, 2),
            }

        upper_limit = next(
            (
                i.value
                for i in CalorieIntakeTiers
                if total_energy_expenditure < i.value
            ),
            CalorieIntakeTiers.TIER_7.value,
        )

        nutritional_bill = MealSummary.objects.order_by(
            "upper_calorie_intake"
        ).filter(diet=user.diet, upper_calorie_intake=upper_limit)

        bill_serializer = MealSummarySerializer(nutritional_bill, many=True)

        results = {
            "weight": user.weight,
            "body_mass_index": round(body_mass_index, 2),
            "bmi_status": bmi_status,
            "weight_goal": user.weight_goal,
            "body_mass_index_goal": round(body_mass_index_goal, 2),
            "bmi_goal_status": bmi_goal_status,
            "healthy_weight_ranges": healthy_weight_ranges,
            "liquid_requirement": liquid_requirement,
            "total_daily_requirement": {
                "get": round(total_energy_expenditure, 2),
                "carbohydrates": round(daily_carbohydrates, 2),
                "carbohydrates_grams": round(daily_carbohydrates_grams, 2),
                "protein": round(daily_protein, 2),
                "protein_grams": round(daily_protein_grams, 2),
                "fats": round(daily_fats, 2),
                "fats_grams": round(daily_fats_grams, 2),
            },
            "meal_distribution": meal_data,
            "nutritional_bill": bill_serializer.data,
        }

        return Response(results, status=status.HTTP_200_OK)


class DailyNutritionalBillCalculationsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrHasMembership]

    def get(self, request):
        meals_data = request.query_params.items()

        results = {"total_calories": 0}

        for meal, food_list in meals_data:
            food_ids = food_list.split(",")
            if not food_list:
                continue

            try:
                food_qs = Food.objects.filter(pk__in=food_ids)
            except ValidationError as e:
                return Response(
                    str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            if food_qs.exists():
                meal_calorie_sum = food_qs.aggregate(Sum("calories"))[
                    "calories__sum"
                ]

                results["total_calories"] += meal_calorie_sum

                if meal in results.keys():
                    results[meal] += meal_calorie_sum
                else:
                    results[meal] = meal_calorie_sum

        return Response(results, status=status.HTTP_200_OK)

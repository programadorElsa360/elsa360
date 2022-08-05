from rest_framework import serializers

from .models import FoodGroup, Food, MealSummary, FoodGroupIntake


class FoodGroupSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        """Validate the supergroup and group relationship."""
        supergroup = attrs["supergroup"]
        group = attrs["group"]
        if group not in FoodGroup.FOOD_SUPERGROUPS_GROUPS[supergroup]:
            raise serializers.ValidationError(
                f"group {group} does not belong to supergroup {supergroup} "
            )

        return attrs

    class Meta:
        model = FoodGroup
        fields = ["supergroup", "group"]


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = [
            "id",
            "name",
            "food_group",
            "cooked_half_portion",
            "raw_half_portion",
            "calories",
            "proteins",
            "fats",
            "carbohydrates",
            "home_measure_amount",
            "home_measure_type",
        ]
        depth = 1


class FoodGroupIntakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodGroupIntake
        fields = ["food_supergroup", "intake"]


class MealSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = MealSummary
        fields = [
            "mealtime",
            "diet",
            "calorie_intake_type",
            "upper_calorie_intake",
            "food_group_intakes",
        ]
        depth = 1

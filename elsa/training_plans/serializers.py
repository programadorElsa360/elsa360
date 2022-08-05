from rest_framework import serializers

from .models import (
    TrainingPlan,
    CyclingPlan,
    PhysicExerciseDescription,
    PhysicPlan,
    QuestionsToPlan,
)


class TrainingPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingPlan
        fields = ["tier"]


class CyclingPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = CyclingPlan
        fields = [
            "training_plan",
            "day",
            "week",
            "cycling_training_time",
            "cycling_training_intensity",
            "cycling_training_percentage",
            "cycling_competition_time",
            "cycling_competition_level",
            "series",
            "series_rest_time",
            "exercise_description",
            "repetitions",
            "repetition_time",
            "repetition_rest_time",
            "return_calm",
            "warming",
            "variables",
        ]
        depth = 1


class PhysicExerciseDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicExerciseDescription
        fields = ["exercise_type", "activities", "description"]


class PhysicPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicPlan
        fields = [
            "training_plan",
            "day",
            "week",
            "gym_training_time",
            "gym_training_intensity",
            "exercise_descriptions",
            "variables",
        ]
        depth = 1


class QuestionsToPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionsToPlan
        fields = [
            "gender",
            "sports_level",
            "sports_goal",
        ]

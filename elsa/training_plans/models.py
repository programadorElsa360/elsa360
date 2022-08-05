from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from elsa.commons.models import (
    UUIDPrimaryKeyModel,
    TimeStampedModel,
)

from elsa.commons.enums import (
    SportsLevels,
    SportsGoals,
    WeekDays,
)

from elsa.users.models import CustomUser


# Create your models here.
class TrainingPlan(UUIDPrimaryKeyModel, TimeStampedModel):
    tier = models.CharField(
        max_length=2,
        choices=SportsLevels.choices,
        default=SportsLevels.BEGINNER,
    )


class QuestionsToPlan(UUIDPrimaryKeyModel, TimeStampedModel):
    gender = models.CharField(
        max_length=2,
        choices=CustomUser.Genders.choices,
        default=CustomUser.Genders.MALE,
    )
    sports_level = models.CharField(
        max_length=2,
        choices=SportsLevels.choices,
        default=SportsLevels.BEGINNER,
    )
    sports_goal = models.CharField(
        max_length=2,
        choices=SportsGoals.choices,
        default=SportsGoals.HEALTH_SOCIAL,
    )

    class Meta:
        unique_together = ["gender", "sports_level", "sports_goal"]


class CyclingPlan(UUIDPrimaryKeyModel, TimeStampedModel):
    class TrainingIntensities(models.IntegerChoices):
        VERY_LIGHT = 4, _("Very light")
        LIGHT = 6, _("Light")
        MODERATE = 8, _("Moderate")
        STRONG = 10, _("Strong")

    class CompetitionLevels(models.IntegerChoices):
        AMATEUR = 12, _("Amateur competition")
        INTERMEDIATE = 14, _("Intermediate competition")
        ADVANCED = 16, _("Advanced competition")

    training_plan = models.ForeignKey(
        to=TrainingPlan, on_delete=models.CASCADE
    )
    day = models.IntegerField(choices=WeekDays.choices)
    week = models.IntegerField(
        validators=[
            MinValueValidator(limit_value=1),
            MaxValueValidator(limit_value=4),
        ],
        default=1,
    )
    cycling_training_time = models.FloatField()
    cycling_training_intensity = models.IntegerField(
        choices=TrainingIntensities.choices,
        default=TrainingIntensities.LIGHT,
    )
    cycling_training_percentage = models.CharField(
        max_length=20, default="LIBRE"
    )
    cycling_competition_time = models.FloatField(null=True, blank=True)
    cycling_competition_level = models.IntegerField(
        choices=CompetitionLevels.choices, null=True, blank=True
    )
    series = models.IntegerField()
    series_rest_time = models.FloatField()
    exercise_description = models.TextField()
    repetitions = models.IntegerField()
    repetition_time = models.FloatField()
    repetition_rest_time = models.FloatField()
    return_calm = models.FloatField()
    warming = models.CharField(max_length=20, null=True, blank=True)
    variables = models.ManyToManyField(to=QuestionsToPlan)


class PhysicExerciseDescription(UUIDPrimaryKeyModel, TimeStampedModel):
    class TrainingTypes(models.TextChoices):
        FULL_STRETCH = "FS", _("Full stretch")
        TRAINING_STRETCH = "TS", _("Training stretch")
        FULL_TRAINING = "FT", _("Full body training")
        UPPER_TRAINING = "UT", _("Upper body training")
        LOWER_TRAINING = "LT", _("Lower body training")
        CORE_TRAINING = "CT", _("Core body training")

    exercise_type = models.CharField(
        max_length=2,
        choices=TrainingTypes.choices,
        default=TrainingTypes.TRAINING_STRETCH,
    )
    activities = models.CharField(max_length=250)
    description = models.TextField()


class PhysicPlan(UUIDPrimaryKeyModel, TimeStampedModel):
    class TrainingIntensities(models.IntegerChoices):
        LIGHT = 3, _("Gym light")
        MODERATE = 4.5, _("Gym moderate")
        STRONG = 6, _("Gym strong")

    training_plan = models.ForeignKey(
        to=TrainingPlan, on_delete=models.CASCADE
    )
    day = models.IntegerField(choices=WeekDays.choices)
    week = models.IntegerField(
        validators=[MaxValueValidator(limit_value=4)], default=1
    )
    gym_training_time = models.FloatField()
    gym_training_intensity = models.IntegerField(
        choices=TrainingIntensities.choices,
        default=TrainingIntensities.LIGHT,
    )
    exercise_descriptions = models.ManyToManyField(
        to=PhysicExerciseDescription
    )
    variables = models.ManyToManyField(to=QuestionsToPlan)

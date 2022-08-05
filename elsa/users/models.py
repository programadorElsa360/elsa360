from datetime import datetime, timezone

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from elsa.psychology.models import BorghEffortScale, BorghSummary

from elsa.commons.enums import (
    BodyGoals,
    BodyTypes,
    DailyTrainingHoursTiers,
    Diet,
    SportsGoals,
    SportsLevels,
    WeeklyTrainingTiers,
)

from elsa.commons.models import TimeStampedModel, UUIDPrimaryKeyModel
from elsa.memberships.models import Coupon, CouponToUser, Membership


# Create your models here.
class CustomUser(AbstractUser, UUIDPrimaryKeyModel, TimeStampedModel):
    """A customer user model containing sports
    and fitness related information alongside the usual user information."""

    class Genders(models.TextChoices):
        MALE = "MA", _("Male")
        FEMALE = "FE", _("Female")

    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False)
    age = models.IntegerField()
    gender = models.CharField(
        max_length=2, choices=Genders.choices, default=Genders.MALE
    )
    height = models.FloatField(help_text="Customer height in centimeters")
    weight = models.FloatField(help_text="Customer weight in kilograms")
    weight_goal = models.FloatField()
    diet = models.CharField(
        max_length=2, choices=Diet.choices, default=Diet.REGULAR
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
    weekly_training = models.CharField(
        max_length=2,
        choices=WeeklyTrainingTiers.choices,
        default=WeeklyTrainingTiers.TIER_1,
    )
    hourly_training = models.CharField(
        max_length=2,
        choices=DailyTrainingHoursTiers.choices,
        default=DailyTrainingHoursTiers.TIER_1,
    )
    body_type = models.CharField(
        max_length=2, choices=BodyTypes.choices, default=BodyTypes.ECTOMORPH
    )
    body_goal = models.CharField(
        max_length=2, choices=BodyGoals.choices, default=BodyGoals.LOSE_WEIGHT
    )
    membership = models.ForeignKey(
        to=Membership, on_delete=models.SET_NULL, null=True, blank=True
    )
    training_start = models.DateTimeField(null=True, blank=True)
    training_end = models.DateTimeField(null=True, blank=True)
    update_info = models.BooleanField(default=False)
    used_coupons = models.ManyToManyField(to=Coupon, through=CouponToUser)
    borgh_historial = models.ManyToManyField(
        to=BorghEffortScale, through=BorghSummary
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def height_in_meters(self):
        return self.height / 100

    @property
    def current_training_day(self):
        current_day = (datetime.now(timezone.utc) - self.training_start).days

        if current_day < 0:
            # If current date is behind the training
            # start date, keep setting it to the 1st
            # day of training.
            current_day = 1
        else:
            current_day += 1

        relative_day = current_day % 7
        if relative_day == 0:
            relative_day = 7

        if self.training_start:
            return {
                "absolute": current_day,
                "relative": relative_day,
            }

        return None

    @property
    def current_training_week(self):
        current_day = self.current_training_day["absolute"]
        if current_day % 7 == 0:
            current_week = current_day // 7
        else:
            current_week = (current_day // 7) + 1

        relative_week = current_week % 4
        if relative_week == 0:
            relative_week = 4

        return {
            "absolute": current_week,
            "relative": relative_week,
        }

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "is_email_verified"]

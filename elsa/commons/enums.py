from django.db.models import IntegerChoices, TextChoices
from django.utils.translation import gettext_lazy as _


class WeekDays(IntegerChoices):
    MONDAY = 1, _("Monday")
    TUESDAY = 2, _("Tuesday")
    WEDNESDAY = 3, _("Wednesday")
    THURSDAY = 4, _("Thursday")
    FRIDAY = 5, _("Friday")
    SATURDAY = 6, _("Saturday")
    SUNDAY = 7, _("Sunday")


class Diet(TextChoices):
    REGULAR = "RG", _("Regular")
    VEGETARIAN = "VE", _("Vegetarian")
    VEGAN = "VG", _("Vegan")


class SportsLevels(TextChoices):
    BEGINNER = "BG", _("Beginner")
    INTERMEDIATE = "IM", _("Intermediate")
    ADVANCED = "AV", _("Advanced")


class SportsGoals(TextChoices):
    PERFORMANCE = "PM", _("Performance")
    HEALTH_SOCIAL = "HS", _("Health / Social")


class WeeklyTrainingTiers(TextChoices):
    TIER_1 = "T1", _("Between 1-2 times weekly")
    TIER_2 = "T2", _("Between 3-4 times weekly")
    TIER_3 = "T3", _("Between 4-5 times weekly")
    TIER_4 = "T4", _("More than 5 times weekly")


class DailyTrainingHoursTiers(TextChoices):
    TIER_1 = "T1", _("Less than 1 hour daily")
    TIER_2 = "T2", _("Between 1-2 hours daily")
    TIER_3 = "T3", _("Between 3-4 hours daily")
    TIER_4 = "T4", _("Between 4-5 hours daily")
    TIER_5 = "T5", _("More than 5 hours daily")


class BodyGoals(TextChoices):
    LOSE_WEIGHT = "LW", _("Lose weight")
    MAINTAIN_WEIGHT = "MW", _("Maintain weight")
    GAIN_MUSCLE = "GM", _("Gain muscle")


class BodyTypes(TextChoices):
    ECTOMORPH = "EC", _("Ectomorph")
    MESOMORPH = "ME", _("Mesomorph")
    ENDOMORPH = "EN", _("Endomorph")


class CalorieIntakeTypes(TextChoices):
    HIPOCALORIC = "HIC", _("Hipocaloric")
    NORMOCALORIC = "NOC", _("Normocaloric")
    HYPERCALORIC = "HYC", _("Hypercaloric")


class CalorieIntakeTiers(IntegerChoices):
    TIER_1 = 1350, _("Between 1200 and 1350 Kcal")
    TIER_2 = 1600, _("Between 1351 and 1600 Kcal")
    TIER_3 = 2000, _("Between 1601 and 2000 Kcal")
    TIER_4 = 2399, _("Between 2001 and 2399 Kcal")
    TIER_5 = 2700, _("Between 2400 and 2700 Kcal")
    TIER_6 = 3050, _("Between 2701 and 3050 Kcal")
    TIER_7 = 3450, _("Between 3051 and 3450 Kcal")


HAMILTON_ANXIETY_SCORE = {
    (0, 17): "Mild anxiety",
    (18, 24): "Moderate anxiety",
    (25, 30): "Severe anxiety",
    (31, 56): "Extreme anxiety",
}

MOOD_GROUP_SCOPES = {
    "international": {
        "tension": 5.66,
        "depression": 4.38,
        "anger": 6.24,
        "vigor": 18.51,
        "fatigue": 5.37,
        "confusion": 4.00,
    },
    "club": {
        "tension": 9.62,
        "depression": 8.67,
        "anger": 9.91,
        "vigor": 15.64,
        "fatigue": 8.16,
        "confusion": 7.38,
    },
    "recreational": {
        "tension": 6.00,
        "depression": 3.11,
        "anger": 3.60,
        "vigor": 17.78,
        "fatigue": 6.37,
        "confusion": 4.84,
    },
}

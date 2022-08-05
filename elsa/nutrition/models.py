from django.db import models
from django.utils.translation import gettext_lazy as _

from elsa.commons.models import (
    UUIDPrimaryKeyModel,
    TimeStampedModel,
)

from elsa.commons.enums import (
    Diet,
    CalorieIntakeTypes,
    CalorieIntakeTiers,
)


class FoodGroup(UUIDPrimaryKeyModel, TimeStampedModel):
    """Nutritional food groups classification."""

    class FoodSuperGroups(models.TextChoices):
        ENERGETIC = "ENE", _("Energetic")
        PROTEIN = "PRO", _("Protein")
        DAIRY = "DAI", _("Dairy")
        LOW_FAT_DAIRY = "LFD", _("Low Fat Dairy")
        FRUITS_AND_VEGGIES = "FAV", _("Fruits & Vegetables")
        HEALTHY_FATS = "HFA", _("Healthy Fats")
        OTHER = "OTH", _("Other")
        NUTRITIONAL_SUPP = "NSU", _("Nutritional Supplements")
        VEGETARIAN_ENE = "VEN", _("Vegetarian Energetic")
        VEGETARIAN_PRO = "VPR", _("Vegetarian Protein")

    class FoodGroups(models.TextChoices):
        CEREALS = "CER", _("Cereals & Derivatives")
        TUBERCULES = "TUB", _("Tubercules")
        PLANTAINS = "PLA", _("Plantains")
        ROOTS = "ROT", _("Roots")
        LEGUMES = "LEG", _("Legumes")
        MEATS = "MEA", _("Red Meats, Chicken, Fish & Eggs")
        MILKS = "MLK", _("Milk & Dairy Derivatives")
        LOW_FAT_MILKS = "LFM", _("Low Fat Milk & Low Fat Dairy Derivatives")
        FRUITS = "FRT", _("Fruits")
        VEGETABLES = "VEG", _("Vegetables")
        SEEDS = "SED", _("Dry Fruits & Seeds")
        POLYSATURATED_FATS = "POL", _("Polysaturated Fats")
        MONOSATURATED_FATS = "MON", _("Monosaturated Fats")
        SATURATED_FATS = "SAT", _("Saturated Fats")
        SUGARS = "SUG", _("Simple Sugars")
        SWEETS = "SWT", _("Sweets & Desserts")
        MISCELLANEOUS = "MIS", _("Miscellaneous")
        PREPARED_FOODS = "PRE", _("Prepared Foods")
        SPICES = "SPI", _("Spices")
        ALCOHOL = "ALH", _("Alcoholic Drinks")
        SUPPLEMENTS = "SUP", _("Nutritional Supplements")
        VEGETARIAN_FOODS = "VGF", _("Vegetarian Foods")
        VEGETARIAN_PROTEIN = "VGP", _("Vegan Protein")
        EGGS = "EGG", _("Eggs")

    FOOD_SUPERGROUPS_GROUPS = {
        FoodSuperGroups.ENERGETIC: [
            FoodGroups.CEREALS,
            FoodGroups.TUBERCULES,
            FoodGroups.PLANTAINS,
            FoodGroups.ROOTS,
            FoodGroups.LEGUMES,
        ],
        FoodSuperGroups.PROTEIN: [FoodGroups.MEATS],
        FoodSuperGroups.DAIRY: [FoodGroups.MILKS],
        FoodSuperGroups.LOW_FAT_DAIRY: [FoodGroups.LOW_FAT_MILKS],
        FoodSuperGroups.FRUITS_AND_VEGGIES: [
            FoodGroups.FRUITS,
            FoodGroups.VEGETABLES,
        ],
        FoodSuperGroups.HEALTHY_FATS: [
            FoodGroups.SEEDS,
            FoodGroups.POLYSATURATED_FATS,
            FoodGroups.MONOSATURATED_FATS,
        ],
        FoodSuperGroups.OTHER: [
            FoodGroups.SATURATED_FATS,
            FoodGroups.SUGARS,
            FoodGroups.SWEETS,
            FoodGroups.MISCELLANEOUS,
            FoodGroups.PREPARED_FOODS,
            FoodGroups.SPICES,
            FoodGroups.ALCOHOL,
        ],
        FoodSuperGroups.NUTRITIONAL_SUPP: [FoodGroups.SUPPLEMENTS],
        FoodSuperGroups.VEGETARIAN_ENE: [
            FoodGroups.CEREALS,
            FoodGroups.TUBERCULES,
            FoodGroups.PLANTAINS,
            FoodGroups.ROOTS,
            FoodGroups.VEGETARIAN_FOODS,
        ],
        FoodSuperGroups.VEGETARIAN_PRO: [
            FoodGroups.VEGETARIAN_PROTEIN,
            FoodGroups.LEGUMES,
            FoodGroups.MILKS,
            FoodGroups.LOW_FAT_MILKS,
            FoodGroups.EGGS,
        ],
    }
    supergroup = models.CharField(
        max_length=3,
        choices=FoodSuperGroups.choices,
        default=FoodSuperGroups.ENERGETIC,
    )
    group = models.CharField(
        max_length=3,
        choices=FoodGroups.choices,
        default=FoodGroups.CEREALS,
    )

    class Meta:
        unique_together = ["supergroup", "group"]


# Create your models here.
class Food(UUIDPrimaryKeyModel, TimeStampedModel):
    class HomeMeasures(models.TextChoices):
        """Commonly used home measures."""

        HEAPING_TABLESPOON = "HP_SP", _("Heaping tablespoon")
        LEVEL_TABLESPOON = "LV_SP", _("Level tablespoon")
        HEAPING_TEASPOON = "HP_TS", _("Heaping teaspoon")
        LEVEL_TEASPOON = "LV_TS", _("Level teaspoon")
        SMALL_MEATBALL = "SM_MT", _("Small meatball")
        SMALL_BALL = "SM_BA", _("Small ball")
        BOTTLE = "BO", _("Bottle")
        EGGYOLK = "EG_YO", _("Egg yolk")
        CUP = "CU", _("Cup")
        LADLE = "LA", _("Ladle")
        SMALL_SEGMENT = "SM_SG", _("Small segment")
        LEAF = "LF", _("Leaf")
        PALM = "PA", _("Palm")
        PILL = "PI", _("Pill")
        SMALL_PLATE = "SM_PL", _("Small plate")
        MEDIUM_PLATE = "MD_PL", _("Medium plate")
        BIG_PLATE = "BG_PL", _("Big plate")
        PERSONAL_PLATE = "PE_PL", _("Personal plate")
        WELL = "WE", _("Well")
        CHOCOLATE_WELL = "CH_WE", _("Chocolate well")
        THIN_SLICES = "TH_SL", _("Thin slices")
        MEDIUM_SLICES = "MD_SL", _("Medium slices")
        BIG_SLICES = "BG_SL", _("Big slices")
        CHOP = "CH", _("Chop")
        THIN_STEMS = "TH_ST", _("Thin stems")
        BOWL = "BW", _("Bowl")
        DRINK = "DR", _("Drink")
        SMALL_CUT = "SM_CT", _("Small cut")
        MEDIUM_CUT = "MD_CT", _("Medium cut")
        BIG_CUT = "BG_CT", _("Big cut")
        SMALL_UNIT = "SM_UN", _("Small unit")
        MEDIUM_UNIT = "MD_UN", _("Medium unit")
        BIG_UNIT = "BG_UN", _("Big unit")
        GLASS = "GL", _("Glass")
        SMALL_GLASS = "SM_GL", _("Small glass")
        MEDIUM_GLASS = "MD_GL", _("Small glass")
        BIG_GLASS = "BG_GL", _("Big glass")
        PERSONAL_CAN = "PE_CN", _("Personal can")
        STRIP = "ST", _("Strip")
        HALVE = "HL", _("Halve")
        PINCH = "PC", _("Pinch")

    name = models.CharField(max_length=100)
    food_group = models.ForeignKey(to=FoodGroup, on_delete=models.CASCADE)
    calories = models.FloatField()
    cooked_half_portion = models.FloatField(help_text="")
    raw_half_portion = models.FloatField(help_text="")
    proteins = models.FloatField()
    fats = models.FloatField()
    carbohydrates = models.FloatField()
    home_measure_amount = models.CharField(max_length=8)
    home_measure_type = models.CharField(
        max_length=5, choices=HomeMeasures.choices, default=HomeMeasures.CUP
    )


class MealSummary(UUIDPrimaryKeyModel, TimeStampedModel):
    class MealTimes(models.IntegerChoices):
        BREAKFAST = 1, _("Breakfast")
        SNACK_1 = 2, "Snack 1"
        LUNCH = 3, _("Lunch")
        SNACK_2 = 4, "Snack 2"
        DINNER = 5, _("Dinner")
        NIGHT_SNACK = 6, _("Night snack")

    mealtime = models.CharField(
        max_length=2, choices=MealTimes.choices, default=MealTimes.BREAKFAST
    )
    diet = models.CharField(
        max_length=2, choices=Diet.choices, default=Diet.REGULAR
    )
    calorie_intake_type = models.CharField(
        max_length=3,
        choices=CalorieIntakeTypes.choices,
        default=CalorieIntakeTypes.NORMOCALORIC,
    )
    upper_calorie_intake = models.IntegerField(
        choices=CalorieIntakeTiers.choices, default=CalorieIntakeTiers.TIER_1
    )

    class Meta:
        unique_together = [
            "mealtime",
            "diet",
            "calorie_intake_type",
            "upper_calorie_intake",
        ]


class FoodGroupIntake(UUIDPrimaryKeyModel, TimeStampedModel):
    food_supergroup = models.CharField(
        max_length=3,
        choices=FoodGroup.FoodSuperGroups.choices,
        default=FoodGroup.FoodSuperGroups.ENERGETIC,
    )
    intake = models.FloatField()
    meal_summary = models.ForeignKey(
        to=MealSummary,
        related_name="food_group_intakes",
        on_delete=models.CASCADE,
    )

import json
import unicodedata
import django
import gspread

from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from configuration.settings.config_utils import get_env_variable

from django.conf import settings


def strip_accents(text):
    text = (
        unicodedata.normalize("NFD", text)
        .encode("ascii", "ignore")
        .decode("utf-8")
    )

    return text


def main():
    django.setup()
    from elsa.nutrition.models import (
        FoodGroup,
        Food,
        MealSummary,
        Diet,
    )
    from elsa.nutrition.serializers import FoodGroupSerializer
    from elsa.commons.enums import CalorieIntakeTiers, CalorieIntakeTypes

    cred_path = Path.home() / get_env_variable("GOOGLE_CREDENTIALS_PATH")
    google_client = gspread.service_account(filename=str(cred_path))

    sheet = google_client.open_by_key(get_env_variable("GS_FOODS_ID"))
    worksheet = sheet.get_worksheet(0)

    regular_food_data, vegan_food_data = worksheet.batch_get(
        ["B5:AD252", "B257:AD338"]
    )
    food_data = regular_food_data + vegan_food_data

    COLUMN_TO_INDEX = {
        "food_supergroup": 0,
        "food_group": 1,
        "food_name": 3,
        "cooked_half_portion": 21,
        "raw_half_portion": 22,
        "calories": 23,
        "proteins": 24,
        "fats": 25,
        "carbohydrates": 26,
        "home_measure_amount": 27,
        "home_measure_type": 28,
    }

    STRING_TO_SUPERGROUP = {
        "ENERGETICOS": FoodGroup.FoodSuperGroups.ENERGETIC,
        "PROTEICOS": FoodGroup.FoodSuperGroups.PROTEIN,
        "LACTEOS": FoodGroup.FoodSuperGroups.DAIRY,
        "LACTEOS BAJOS EN GRASA": FoodGroup.FoodSuperGroups.LOW_FAT_DAIRY,
        "FRUTAS Y VERDURAS": FoodGroup.FoodSuperGroups.FRUITS_AND_VEGGIES,
        "GRASAS SALUDABLES": FoodGroup.FoodSuperGroups.HEALTHY_FATS,
        "SUPLEMENTOS NUTRICIONALES": FoodGroup.FoodSuperGroups.NUTRITIONAL_SUPP,
        "ENERGETICOS VEGETARIANOS": FoodGroup.FoodSuperGroups.VEGETARIAN_ENE,
        "PROTEICOS VEGETARIANOS": FoodGroup.FoodSuperGroups.VEGETARIAN_PRO,
        "OTROS": FoodGroup.FoodSuperGroups.OTHER,
    }

    STRING_TO_GROUP = {
        "CEREALES Y DERIVADOS": FoodGroup.FoodGroups.CEREALS,
        "TUBÉRCULOS": FoodGroup.FoodGroups.TUBERCULES,
        "PLÁTANOS": FoodGroup.FoodGroups.PLANTAINS,
        "RAÍCES": FoodGroup.FoodGroups.ROOTS,
        "LEGUMINOSAS": FoodGroup.FoodGroups.LEGUMES,
        "CARNES, POLLO, PESCADOS Y HUEVOS": FoodGroup.FoodGroups.MEATS,
        "LECHE Y DERIVADOS LÁCTEOS": FoodGroup.FoodGroups.MILKS,
        "LECHE Y DERIVADOS LÁCTEOS BAJOS EN GRASA": FoodGroup.FoodGroups.LOW_FAT_MILKS,
        "VERDURAS": FoodGroup.FoodGroups.VEGETABLES,
        "FRUTAS": FoodGroup.FoodGroups.FRUITS,
        "FRUTOS SECOS Y SEMILLAS": FoodGroup.FoodGroups.SEEDS,
        "GRASAS POLIINSATURADAS": FoodGroup.FoodGroups.POLYSATURATED_FATS,
        "GRASAS MONOINSATURADAS": FoodGroup.FoodGroups.MONOSATURATED_FATS,
        "GRASAS SATURADAS": FoodGroup.FoodGroups.SATURATED_FATS,
        "AZÚCARES SIMPLES": FoodGroup.FoodGroups.SUGARS,
        "DULCES Y POSTRES": FoodGroup.FoodGroups.SWEETS,
        "MISCELÁNEOS": FoodGroup.FoodGroups.MISCELLANEOUS,
        "ALIMENTOS PREPARADOS": FoodGroup.FoodGroups.PREPARED_FOODS,
        "ESPECIAS": FoodGroup.FoodGroups.SPICES,
        "BEBIDAS ALCOHOLICAS": FoodGroup.FoodGroups.ALCOHOL,
        "SUPLEMENTOS NUTRICIONALES": FoodGroup.FoodGroups.SUPPLEMENTS,
        "ALIMENTOS VEGETARIANOS": FoodGroup.FoodGroups.VEGETARIAN_FOODS,
        "PROTEICOS VEGANOS": FoodGroup.FoodGroups.VEGETARIAN_PROTEIN,
        "HUEVOS": FoodGroup.FoodGroups.EGGS,
    }

    STRING_TO_MEASURE = {
        "cdas colmadas": Food.HomeMeasures.HEAPING_TABLESPOON,
        "cdas rasas": Food.HomeMeasures.LEVEL_TABLESPOON,
        "cditas colmadas": Food.HomeMeasures.HEAPING_TEASPOON,
        "cditas rasas": Food.HomeMeasures.LEVEL_TEASPOON,
        "pocillo chocolatero": Food.HomeMeasures.CHOCOLATE_WELL,
        "Pocillo chocolatero": Food.HomeMeasures.CHOCOLATE_WELL,
        "Unidad pequeña": Food.HomeMeasures.SMALL_UNIT,
        "Unidad mediana": Food.HomeMeasures.MEDIUM_UNIT,
        "Unidad grande": Food.HomeMeasures.BIG_UNIT,
        "Unidad": Food.HomeMeasures.MEDIUM_UNIT,
        "Tajada": Food.HomeMeasures.CHOP,
        "Trozo pequeño": Food.HomeMeasures.SMALL_CUT,
        "Trozo mediano": Food.HomeMeasures.MEDIUM_CUT,
        "Trozo grande": Food.HomeMeasures.BIG_CUT,
        "Cucharon": Food.HomeMeasures.LADLE,
        "Palma de una mano": Food.HomeMeasures.PALM,
        "Rodajas delgadas": Food.HomeMeasures.THIN_SLICES,
        "Rodajas medianas": Food.HomeMeasures.MEDIUM_SLICES,
        "Rodajas grandes": Food.HomeMeasures.BIG_SLICES,
        "Albondiga Pequeña": Food.HomeMeasures.SMALL_MEATBALL,
        "Claras": Food.HomeMeasures.EGGYOLK,
        "Vaso pequeño": Food.HomeMeasures.SMALL_GLASS,
        "Vaso mediano": Food.HomeMeasures.MEDIUM_GLASS,
        "Vaso Grande": Food.HomeMeasures.BIG_GLASS,
        "taza": Food.HomeMeasures.GLASS,
        "Tallos delgados": Food.HomeMeasures.THIN_STEMS,
        "Gajos/Arbolitos pequeños": Food.HomeMeasures.SMALL_SEGMENT,
        "Hojas": Food.HomeMeasures.LEAF,
        "Tira": Food.HomeMeasures.STRIP,
        "Bola pequeña": Food.HomeMeasures.SMALL_BALL,
        "Mitades": Food.HomeMeasures.HALVE,
        "Pastilla": Food.HomeMeasures.PILL,
        "Plato grande": Food.HomeMeasures.BIG_PLATE,
        "Plato personal": Food.HomeMeasures.PERSONAL_PLATE,
        "Pizca": Food.HomeMeasures.PINCH,
        "Botella": Food.HomeMeasures.BOTTLE,
        "Copa": Food.HomeMeasures.CUP,
        "Trago": Food.HomeMeasures.DRINK,
    }

    food_groups_json_data = []
    food_json_data = []
    for row in food_data:
        # Remove trailing whitespace.
        row = [x.strip() for x in row]

        parsed_supergroup = row[COLUMN_TO_INDEX["food_supergroup"]]
        parsed_group = row[COLUMN_TO_INDEX["food_group"]]
        if parsed_supergroup:
            current_supergroup = STRING_TO_SUPERGROUP[parsed_supergroup]

        if parsed_group:
            current_group = STRING_TO_GROUP[parsed_group]

        if parsed_supergroup or parsed_group:
            food_group_pk = str(uuid4())
            food_groups_json_data.append(
                {
                    "model": "nutrition.FoodGroup",
                    "pk": food_group_pk,
                    "fields": {
                        "supergroup": current_supergroup,
                        "group": current_group,
                        "created_at": str(datetime.now(timezone.utc)),
                        "updated_at": str(datetime.now(timezone.utc)),
                    },
                }
            )

        food_name = row[COLUMN_TO_INDEX["food_name"]]
        calories = float(row[COLUMN_TO_INDEX["calories"]])
        cooked_portion = float(row[COLUMN_TO_INDEX["cooked_half_portion"]])
        raw_portion = float(row[COLUMN_TO_INDEX["raw_half_portion"]])
        proteins = float(row[COLUMN_TO_INDEX["proteins"]])
        fats = float(row[COLUMN_TO_INDEX["fats"]])
        carbohydrates = float(row[COLUMN_TO_INDEX["carbohydrates"]])

        measure_amount = row[COLUMN_TO_INDEX["home_measure_amount"]]
        measure_type = STRING_TO_MEASURE[
            row[COLUMN_TO_INDEX["home_measure_type"]]
        ]

        food_json_data.append(
            {
                "model": "nutrition.Food",
                "pk": str(uuid4()),
                "fields": {
                    "name": food_name,
                    "food_group": food_group_pk,
                    "calories": calories,
                    "cooked_half_portion": cooked_portion,
                    "raw_half_portion": raw_portion,
                    "proteins": proteins,
                    "fats": fats,
                    "carbohydrates": carbohydrates,
                    "home_measure_amount": measure_amount,
                    "home_measure_type": measure_type,
                    "created_at": str(datetime.now(timezone.utc)),
                    "updated_at": str(datetime.now(timezone.utc)),
                },
            }
        )

    # Validate data.
    food_group_serializer = FoodGroupSerializer(
        data=food_groups_json_data, many=True
    )

    if not food_group_serializer.is_valid():
        print(json.dumps(food_group_serializer.errors, indent=4))

    # Parse food minutes
    worksheet = sheet.get_worksheet(1)
    minute_data = worksheet.batch_get(
        [
            "B4:D24",
            "B34:D54",
            "F4:H24",
            "F34:H54",
            "J4:L28",
            "J34:L58",
            "J63:L88",
            "P4:R20",
            "P34:R50",
            "T4:V20",
            "T34:V50",
            "X4:Z24",
            "X34:Z54",
            "X59:Z79",
        ]
    )

    COLUMN_TO_INDEX_2 = {"meal": 0, "supergroup": 1, "amount": 2}
    STRING_TO_MEAL = {
        "Desayuno": MealSummary.MealTimes.BREAKFAST,
        "Snack 1": MealSummary.MealTimes.SNACK_1,
        "Almuerzo": MealSummary.MealTimes.LUNCH,
        "Snack 2": MealSummary.MealTimes.SNACK_2,
        "Cena": MealSummary.MealTimes.DINNER,
        "Refrigerio nocturno": MealSummary.MealTimes.NIGHT_SNACK,
    }

    diets = [Diet.REGULAR for i in range(7)] + [
        Diet.VEGETARIAN for i in range(7)
    ]
    calorie_intakes = list(CalorieIntakeTiers) + list(CalorieIntakeTiers)

    calorie_types = [
        [tier for i in range(times)]
        for tier, times in zip(list(CalorieIntakeTypes), [2, 2, 3])
    ]
    # Flatten and duplicate list
    calorie_types = [x for sublist in calorie_types for x in sublist]
    calorie_types += calorie_types

    full_data = list(zip(minute_data, diets, calorie_types, calorie_intakes))
    meal_json = []
    intakes_json = []
    for data, diet, calorie_type, calorie_tier in full_data:
        for row in data:
            # Skip empty rows.
            if len(row) == 0:
                continue
            # Remove trailing whitespace.
            row = [x.strip() for x in row]

            parsed_meal = row[COLUMN_TO_INDEX_2["meal"]]
            if parsed_meal:
                current_meal = STRING_TO_MEAL[parsed_meal]

                meal_pk = str(uuid4())
                meal_data = {
                    "uuid": meal_pk,
                    "mealtime": current_meal,
                    "diet": diet,
                    "calorie_intake_type": calorie_type,
                    "upper_calorie_intake": calorie_tier,
                }
                meal_data.pop("uuid")
                meal_json.append(
                    {
                        "model": "nutrition.MealSummary",
                        "pk": meal_pk,
                        "fields": {
                            **meal_data,
                            "created_at": str(datetime.now(timezone.utc)),
                            "updated_at": str(datetime.now(timezone.utc)),
                        },
                    }
                )

            supergroup = STRING_TO_SUPERGROUP[
                strip_accents(row[COLUMN_TO_INDEX_2["supergroup"]]).upper()
            ]
            amount = float(row[COLUMN_TO_INDEX_2["amount"]])

            intake_pk = str(uuid4())
            intake_data = {
                "uuid": intake_pk,
                "food_supergroup": supergroup,
                "intake": amount,
                "meal_summary": meal_pk,
            }
            intake_data.pop("uuid")
            intakes_json.append(
                {
                    "model": "nutrition.FoodGroupIntake",
                    "pk": intake_pk,
                    "fields": {
                        **intake_data,
                        "created_at": str(datetime.now(timezone.utc)),
                        "updated_at": str(datetime.now(timezone.utc)),
                    },
                }
            )

    fixtures_path = settings.BASE_DIR / "elsa" / "nutrition" / "fixtures"

    with open(fixtures_path / "initial_data.json", "w", encoding="utf-8") as f:
        json.dump(
            food_groups_json_data + food_json_data,
            f,
            ensure_ascii=False,
            indent=2,
        )

    with open(
        fixtures_path / "nutritional_minutes.json", "w", encoding="utf-8"
    ) as f:
        json.dump(
            meal_json + intakes_json,
            f,
            ensure_ascii=False,
            indent=2,
        )


if __name__ == "__main__":
    main()

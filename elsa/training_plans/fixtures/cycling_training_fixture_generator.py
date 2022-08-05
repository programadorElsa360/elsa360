import json
import django
import gspread

from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from configuration.settings.config_utils import get_env_variable

from django.conf import settings


def parse_float(string: str):
    if not string or string.upper() == "LIBRE" or string == "NA":
        return 0.0
    else:
        number, _ = string.split(" ")
        return float(number)


def main():
    django.setup()
    from elsa.commons.enums import SportsGoals, SportsLevels
    from elsa.training_plans.models import (
        CyclingPlan,
        TrainingPlan,
        QuestionsToPlan,
    )
    from elsa.users.models import CustomUser

    cred_path = Path.home() / get_env_variable("GOOGLE_CREDENTIALS_PATH")
    google_client = gspread.service_account(filename=str(cred_path))

    sheet_ids = [
        get_env_variable("GS_TRAINING_MEN_WOMAN_BEGINNER_PERF_ID"),
        get_env_variable("GS_TRAINING_MEN_INTERMEDIATE_PERF_ID"),
        get_env_variable("GS_TRAINING_WOMAN_INTERMEDIATE_PERF_ID"),
        get_env_variable("GS_TRAINING_MEN_WOMAN_ADVANCED_PERF_ID"),
        get_env_variable("GS_TRAINING_MEN_WOMAN_BEGINNER_HEALTH_ID"),
        get_env_variable("GS_TRAINING_MEN_INTERMEDIATE_HEALTH_ID"),
        get_env_variable("GS_TRAINING_WOMAN_INTERMEDIATE_HEALTH_ID"),
        get_env_variable("GS_TRAINING_MEN_WOMAN_ADVANCED_HEALTH_ID"),
    ]
    ranges = [
        ["B5:N11", "B16:N22", "B27:N33", "B38:N44", "P4:R8"],  # Performance
        ["B5:N11", "B16:N22", "B27:N33", "B38:N44", "P4:R8"],
        ["B5:N11", "B16:N22", "B27:N33", "B38:N44", "P4:R8"],
        ["B5:N11", "B17:N24", "B29:N35", "B40:N46", "P4:R8"],
        ["B5:N11", "B17:N23", "B29:N35", "B41:N47", "P4:R8"],  # Health
        ["B5:N11", "B17:N23", "B29:N35", "B41:N47", "P4:R8"],
        ["B5:N11", "B17:N23", "B29:N35", "B41:N47", "P4:R8"],
        ["B5:N11", "B17:N23", "B29:N35", "B41:N47", "P4:R8"],
    ]
    sheets = list(map(google_client.open_by_key, sheet_ids))
    sheets = list(zip(sheets, ranges))

    COLUMN_TO_INDEX = {
        "day": 0,
        "warming": 2,
        "series": 3,
        "series_rest_time": 4,
        "repetitions": 5,
        "repetitions_time": 6,
        "repetitions_rest_time": 7,
        "description": 8,
        "cycling_training_percentage": 9,
        "cycling_training_intensity": 10,
        "return_calm": 11,
        "cycling_training_time": 12,
    }
    STRING_TO_SPORTS_LVL = {
        "Principiante": SportsLevels.BEGINNER,
        "Intermedio": SportsLevels.INTERMEDIATE,
        "Avanzado": SportsLevels.ADVANCED,
    }
    STRING_TO_SPORTS_GOAL = {
        "Rendimiento": SportsGoals.PERFORMANCE,
        "Saludable/Ocio": SportsGoals.HEALTH_SOCIAL,
    }
    STRING_TO_GENDER = {
        "Hombre": CustomUser.Genders.MALE,
        "Mujer": CustomUser.Genders.FEMALE,
    }
    STRING_TO_INTENSITY = {
        "Intensidad Muy Leve": CyclingPlan.TrainingIntensities.VERY_LIGHT,
        "Intensidad Leve": CyclingPlan.TrainingIntensities.LIGHT,
        "Intensidad Moderada": CyclingPlan.TrainingIntensities.MODERATE,
        "Intensidad Fuerte": CyclingPlan.TrainingIntensities.STRONG,
    }

    training_json_data = []
    for sheet, sheet_ranges in sheets:
        worksheet = sheet.get_worksheet(0)

        (
            week1_data,
            week2_data,
            week3_data,
            week4_data,
            variables_data,
        ) = worksheet.batch_get(sheet_ranges)
        week_data = [week1_data, week2_data, week3_data, week4_data]

        variables_data = [x for x in variables_data if len(x) > 0]
        parsed_sports_lvl = variables_data[0][1]
        parsed_genders = variables_data[1][1:3]
        parsed_goal = variables_data[2][1]

        sports_lvl = STRING_TO_SPORTS_LVL[parsed_sports_lvl]
        genders = [
            STRING_TO_GENDER[parsed_gender] for parsed_gender in parsed_genders
        ]
        sports_goal = STRING_TO_SPORTS_GOAL[parsed_goal]

        training_plan = TrainingPlan.objects.get(tier=sports_lvl.value)
        for count, week in enumerate(week_data):
            for row in week:
                # Ignore empty rows.
                if len(row) < 13:
                    continue
                # Remove trailing whitespace.
                row = [x.strip() for x in row]

                cycling_plan_pk = str(uuid4())
                day = int(row[COLUMN_TO_INDEX["day"]])

                cycling_training_time = parse_float(
                    row[COLUMN_TO_INDEX["cycling_training_time"]]
                )
                cycling_training_intensity = STRING_TO_INTENSITY[
                    row[COLUMN_TO_INDEX["cycling_training_intensity"]].title()
                ]
                cycling_training_percentage = row[
                    COLUMN_TO_INDEX["cycling_training_percentage"]
                ]

                parsed_series = row[COLUMN_TO_INDEX["series"]]
                if not parsed_series:
                    series = 0
                else:
                    series = int(parsed_series)

                series_rest_time = parse_float(
                    row[COLUMN_TO_INDEX["series_rest_time"]]
                )
                description = row[COLUMN_TO_INDEX["description"]].capitalize()

                parsed_repetitions = row[COLUMN_TO_INDEX["repetitions"]]
                if not parsed_repetitions:
                    repetitions = 0
                else:
                    repetitions = int(parsed_repetitions)

                repetitions_time = parse_float(
                    row[COLUMN_TO_INDEX["repetitions_time"]]
                )

                repetitions_rest_time = parse_float(
                    row[COLUMN_TO_INDEX["repetitions_rest_time"]]
                )

                return_calm = parse_float(row[COLUMN_TO_INDEX["return_calm"]])
                warming = row[COLUMN_TO_INDEX["warming"]]

                plan_map = QuestionsToPlan.objects.filter(
                    gender__in=genders,
                    sports_level=sports_lvl,
                    sports_goal=sports_goal,
                )
                if not plan_map.exists():
                    raise Exception(
                        "No QuestionsToPlan instance available to update."
                    )

                if len(plan_map) > 2:
                    raise Exception(
                        "There can be at most 2 instances of QuestionsToPlan."
                    )

                data = {
                    "uuid": cycling_plan_pk,
                    "training_plan": str(training_plan.pk),
                    "day": day,
                    "week": count + 1,
                    "cycling_training_time": cycling_training_time,
                    "cycling_training_intensity": cycling_training_intensity,
                    "cycling_training_percentage": cycling_training_percentage,
                    "series": series,
                    "series_rest_time": series_rest_time,
                    "exercise_description": description,
                    "repetitions": repetitions,
                    "repetition_time": repetitions_time,
                    "repetition_rest_time": repetitions_rest_time,
                    "return_calm": return_calm,
                    "warming": warming,
                    "variables": [
                        str(d["pk"]) for d in list(plan_map.values("pk"))
                    ],
                }
                data.pop("uuid")
                training_json_data.append(
                    {
                        "model": "training_plans.CyclingPlan",
                        "pk": cycling_plan_pk,
                        "fields": {
                            **data,
                            "created_at": str(datetime.now(timezone.utc)),
                            "updated_at": str(datetime.now(timezone.utc)),
                        },
                    }
                )

    json_file_path = (
        settings.BASE_DIR
        / "elsa"
        / "training_plans"
        / "fixtures"
        / "cycling_trainings.json"
    )
    with open(json_file_path, "w", encoding="utf-8") as f:
        json.dump(training_json_data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()

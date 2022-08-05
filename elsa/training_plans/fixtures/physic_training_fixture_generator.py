import json

from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import django
import gspread

from configuration.settings.config_utils import get_env_variable

from django.conf import settings


def main():
    django.setup()
    from elsa.commons.enums import SportsGoals, SportsLevels
    from elsa.training_plans.models import (
        TrainingPlan,
        PhysicPlan,
        PhysicExerciseDescription,
        QuestionsToPlan,
    )
    from elsa.training_plans.serializers import PhysicPlanSerializer
    from elsa.users.models import CustomUser

    cred_path = Path.home() / get_env_variable("GOOGLE_CREDENTIALS_PATH")
    google_client = gspread.service_account(filename=str(cred_path))

    # Parse training plans.
    plans_sheet_ids = [
        get_env_variable("GS_GYM_TRAINING_MEN_WOMAN_BEGINNER_PERF_ID"),
        get_env_variable("GS_GYM_TRAINING_MEN_BEGINNER_PERF_ID"),
        get_env_variable("GS_GYM_TRAINING_WOMAN_INTERMEDIATE_PERF_ID"),
        get_env_variable("GS_GYM_TRAINING_MEN_WOMAN_ADVANCED_PERF_ID"),
        get_env_variable("GS_GYM_TRAINING_MEN_WOMAN_BEGINNER_HEALTH_ID"),
        get_env_variable("GS_GYM_TRAINING_MEN_INTERMEDIATE_HEALTH_ID"),
        get_env_variable("GS_GYM_TRAINING_WOMAN_INTERMEDIATE_HEALTH_ID"),
        get_env_variable("GS_GYM_TRAINING_MEN_WOMAN_ADVANCED_HEALTH_ID"),
    ]
    ranges = [
        ["B5:F11", "B16:F22", "B27:F33", "B38:F44", "I4:J8"],
        ["B5:F11", "B16:F22", "B27:F33", "B38:F44", "I4:J8"],
        ["B5:F11", "B16:F22", "B27:F33", "B38:F44", "I4:J8"],
        ["B5:F11", "B16:F22", "B27:F33", "B38:F44", "I4:J8"],
        ["B5:F11", "B17:F23", "B29:F35", "B41:F47", "I4:J8"],
        ["B5:F11", "B17:F23", "B29:F35", "B41:F47", "I4:J8"],
        ["B5:F11", "B17:F23", "B29:F35", "B41:F47", "I4:J8"],
        ["B5:F11", "B17:F23", "B29:F35", "B41:F47", "I4:J8"],
    ]

    PLANS_COLUMN_TO_INDEX = {
        "day": 0,
        "descriptions": 2,
        "intensity": 3,
        "training_time": 4,
    }
    STRING_TO_INTENSITY = {
        "GYM-Suave": PhysicPlan.TrainingIntensities.LIGHT,
        "GYM-Moderado": PhysicPlan.TrainingIntensities.MODERATE,
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
    STRING_TO_DESCRIPTION = {
        "ESTIRAMIENTO PARA ENTRENAR (Training stretch)": PhysicExerciseDescription.TrainingTypes.TRAINING_STRETCH,
        "ESTIRAMIENTO COMPLETO (Full Body)": PhysicExerciseDescription.TrainingTypes.FULL_STRETCH,
        "ENTRENO CORE": PhysicExerciseDescription.TrainingTypes.CORE_TRAINING,
        "ENTRENO TREN SUPERIOR": PhysicExerciseDescription.TrainingTypes.UPPER_TRAINING,
        "ENTRENO TREN INFERIOR": PhysicExerciseDescription.TrainingTypes.LOWER_TRAINING,
        "ENTRENO CUERPO COMPLETO": PhysicExerciseDescription.TrainingTypes.FULL_TRAINING,
    }

    sheets = list(map(google_client.open_by_key, plans_sheet_ids))
    sheets = list(zip(sheets, ranges))

    physic_plans_json = []
    for sheet, ranges in sheets:
        worksheet = sheet.get_worksheet(0)
        (
            week1_data,
            week2_data,
            week3_data,
            week4_data,
            variables_data,
        ) = worksheet.batch_get(ranges)
        week_data = [week1_data, week2_data, week3_data, week4_data]

        variables_data = [x for x in variables_data if len(x) > 0]
        parsed_sports_lvl = variables_data[0][0]
        parsed_genders = variables_data[1][0:2]
        parsed_goal = variables_data[2][0]

        sports_lvl = STRING_TO_SPORTS_LVL[parsed_sports_lvl]
        genders = [
            STRING_TO_GENDER[parsed_gender] for parsed_gender in parsed_genders
        ]
        sports_goal = STRING_TO_SPORTS_GOAL[parsed_goal]

        training_plan = TrainingPlan.objects.get(tier=sports_lvl.value)
        for count, week in enumerate(week_data):
            for row in week:
                # Ignore empty rows.
                if len(row) == 0:
                    continue
                # Remove trailing whitespace.
                row = [x.strip() for x in row]

                physic_plan_pk = str(uuid4())
                day = int(row[PLANS_COLUMN_TO_INDEX["day"]])
                training_time = float(
                    row[PLANS_COLUMN_TO_INDEX["training_time"]]
                )
                training_intensity = STRING_TO_INTENSITY[
                    row[PLANS_COLUMN_TO_INDEX["intensity"]]
                ]

                descriptions = row[
                    PLANS_COLUMN_TO_INDEX["descriptions"]
                ].split("+")
                descriptions = [
                    STRING_TO_DESCRIPTION[d.strip()] for d in descriptions
                ]

                def find_descriptions(
                    desc_type: PhysicExerciseDescription.TrainingTypes,
                ):
                    primary_keys = PhysicExerciseDescription.objects.filter(
                        exercise_type=desc_type
                    ).values("pk")
                    return [str(dict["pk"]) for dict in primary_keys]

                descriptions_uuids = [
                    find_descriptions(d) for d in descriptions
                ]

                for _, desc_uuids in zip(descriptions, descriptions_uuids):
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
                            "There can be at most 2 "
                            + "instances of QuestionsToPlan."
                        )

                    data = {
                        "uuid": physic_plan_pk,
                        "training_plan": str(training_plan.pk),
                        "day": day,
                        "week": count + 1,
                        "gym_training_time": training_time,
                        "gym_training_intensity": training_intensity,
                        "exercise_descriptions": desc_uuids,
                        "variables": [
                            str(d["pk"]) for d in list(plan_map.values("pk"))
                        ],
                    }
                    data.pop("uuid")
                    json_data = {
                        "model": "training_plans.PhysicPlan",
                        "pk": physic_plan_pk,
                        "fields": {
                            **data,
                            "created_at": str(datetime.now(timezone.utc)),
                            "updated_at": str(datetime.now(timezone.utc)),
                        },
                    }
                    physic_plans_json.append(json_data)

                    # Save instance in DB.
                    physic_serializer = PhysicPlanSerializer(data=data)
                    physic_serializer.is_valid(raise_exception=True)

    json_file_path = (
        settings.BASE_DIR
        / "elsa"
        / "training_plans"
        / "fixtures"
        / "physic_trainings.json"
    )
    with open(json_file_path, "w", encoding="utf-8") as f:
        json.dump(physic_plans_json, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()

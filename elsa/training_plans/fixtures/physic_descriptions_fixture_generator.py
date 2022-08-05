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
    from elsa.training_plans.models import PhysicExerciseDescription
    from elsa.training_plans.serializers import PhysicExerciseDescriptionSerializer

    cred_path = Path.home() / get_env_variable("GOOGLE_CREDENTIALS_PATH")
    google_client = gspread.service_account(filename=str(cred_path))

    # Parse training descriptions.
    sheet = google_client.open_by_key(
        get_env_variable("GS_GYM_TRAINING_DESCRIPTIONS_ID")
    )
    worksheet = sheet.get_worksheet(0)

    COLUMN_TO_INDEX = {"activities": 0, "description": 1}

    (
        full_stretch_data,
        training_stretch_data,
        full_train_data,
        upper_train_data,
        lower_train_data,
        core_train_data,
    ) = worksheet.batch_get(
        ["C3:D14", "C19:D25", "C29:D35", "C39:D45", "C49:D51", "C55:D49"]
    )

    def parse_row(row, training_type: PhysicExerciseDescription.GymTrainingTypes):
        row = [x.strip() for x in row]

        activities = row[COLUMN_TO_INDEX["activities"]]
        description = row[COLUMN_TO_INDEX["description"]]

        return {
            "model": "training_plans.PhysicExerciseDescription",
            "pk": str(uuid4()),
            "fields": {
                "exercise_type": training_type,
                "activities": activities,
                "description": description,
                "created_at": str(datetime.now(timezone.utc)),
                "updated_at": str(datetime.now(timezone.utc)),
            },
        }

    full_stretch_json = [
        parse_row(r, PhysicExerciseDescription.GymTrainingTypes.FULL_STRETCH)
        for r in filter(lambda x: len(x) != 0, full_stretch_data)
    ]
    training_stretch_json = [
        parse_row(r, PhysicExerciseDescription.GymTrainingTypes.TRAINING_STRETCH)
        for r in filter(lambda x: len(x) != 0, training_stretch_data)
    ]
    full_training_json = [
        parse_row(r, PhysicExerciseDescription.GymTrainingTypes.FULL_TRAINING)
        for r in filter(lambda x: len(x) != 0, full_train_data)
    ]
    upper_training_json = [
        parse_row(r, PhysicExerciseDescription.GymTrainingTypes.UPPER_TRAINING)
        for r in filter(lambda x: len(x) != 0, upper_train_data)
    ]
    lower_training_json = [
        parse_row(r, PhysicExerciseDescription.GymTrainingTypes.LOWER_TRAINING)
        for r in filter(lambda x: len(x) != 0, lower_train_data)
    ]
    core_training_json = [
        parse_row(r, PhysicExerciseDescription.GymTrainingTypes.CORE_TRAINING)
        for r in filter(lambda x: len(x) != 0, core_train_data)
    ]

    descriptions_json = (
        full_stretch_json
        + training_stretch_json
        + full_training_json
        + upper_training_json
        + lower_training_json
        + core_training_json
    )

    desc_serializer = PhysicExerciseDescriptionSerializer(
        data=[x["fields"] for x in descriptions_json], many=True
    )

    if not desc_serializer.is_valid():
        print(json.dumps(desc_serializer.errors))

    json_file_path = (
        settings.BASE_DIR
        / "elsa"
        / "training_plans"
        / "fixtures"
        / "physic_descriptions.json"
    )
    with open(json_file_path, "w", encoding="utf-8") as f:
        json.dump(descriptions_json, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()

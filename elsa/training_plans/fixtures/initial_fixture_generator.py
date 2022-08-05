import django
import json

from datetime import datetime, timezone
from uuid import uuid4
from itertools import product

from django.conf import settings


def main():
    django.setup()
    from elsa.training_plans.models import SportsLevels, SportsGoals
    from elsa.training_plans.serializers import (
        TrainingPlanSerializer,
        QuestionsToPlanSerializer,
    )
    from elsa.users.models import CustomUser

    training_data = []
    questions_data = []
    json_data = []

    for level in list(SportsLevels):
        pk = str(uuid4())
        data = {
            "uuid": pk,
            "tier": level.value,
        }
        training_data.append(data)
        data.pop("uuid")
        json_data.append(
            {
                "model": "training_plans.TrainingPlan",
                "pk": pk,
                "fields": {
                    **data,
                    "created_at": str(datetime.now(timezone.utc)),
                    "updated_at": str(datetime.now(timezone.utc)),
                },
            }
        )

    serializer = TrainingPlanSerializer(data=training_data, many=True)
    serializer.is_valid(raise_exception=True)

    genders_levels = list(product(CustomUser.Genders, SportsLevels))
    genders_levels_goals = [
        (a, b, c) for (a, b), c in list(product(genders_levels, SportsGoals))
    ]

    for gender, level, goal in genders_levels_goals:
        pk = str(uuid4())
        data = {
            "uuid": pk,
            "gender": gender,
            "sports_level": level,
            "sports_goal": goal,
        }
        data.pop("uuid")
        questions_data.append(data)
        json_data.append(
            {
                "model": "training_plans.QuestionsToPlan",
                "pk": pk,
                "fields": {
                    **data,
                    "created_at": str(datetime.now(timezone.utc)),
                    "updated_at": str(datetime.now(timezone.utc)),
                },
            }
        )

    serializer = QuestionsToPlanSerializer(data=questions_data, many=True)
    serializer.is_valid(raise_exception=True)

    json_file_path = (
        settings.BASE_DIR / "elsa" / "training_plans" / "fixtures" / "initial_data.json"
    )
    with open(json_file_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()

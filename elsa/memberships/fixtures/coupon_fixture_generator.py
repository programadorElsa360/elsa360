import json

import django
import gspread

from datetime import datetime, timezone
from uuid import uuid4
from pathlib import Path

from django.conf import settings

from configuration.settings.config_utils import get_env_variable


def main():
    django.setup()

    from elsa.memberships.serializers import CouponSerializer

    cred_path = Path.home() / get_env_variable("GOOGLE_CREDENTIALS_PATH")
    google_client = gspread.service_account(filename=str(cred_path))

    sheet = google_client.open_by_key(get_env_variable("GS_COUPONS_ID"))
    worksheet = sheet.get_worksheet(0)

    sheet_data = worksheet.batch_get(["C3:F99"])[0]

    COLUMN_TO_INDEX = {
        "code": 0,
        "discount": 1,
        "start_date": 2,
        "end_date": 3,
    }

    coupon_data = []
    coupons_json = []
    for row in sheet_data:
        code = row[COLUMN_TO_INDEX["code"]]
        discount = float(row[COLUMN_TO_INDEX["discount"]].split("%")[0]) / 100
        start_date = row[COLUMN_TO_INDEX["start_date"]]
        end_date = row[COLUMN_TO_INDEX["end_date"]]

        pk = str(uuid4())
        data = {
            "uuid": pk,
            "name": code,
            "discount": discount,
            "valid_start_date": str(
                datetime.fromisoformat(start_date).astimezone(timezone.utc)
            ),
            "valid_end_date": str(
                datetime.fromisoformat(end_date).astimezone(timezone.utc)
            ),
        }
        coupon_data.append(data)
        data.pop("uuid")
        coupons_json.append(
            {
                "model": "memberships.Coupon",
                "pk": pk,
                "fields": {
                    **data,
                    "created_at": str(datetime.now(timezone.utc)),
                    "updated_at": str(datetime.now(timezone.utc)),
                },
            }
        )

    serializer = CouponSerializer(data=coupon_data, many=True)
    serializer.is_valid(raise_exception=True)

    fixtures_path = settings.BASE_DIR / "elsa" / "memberships" / "fixtures"

    with open(fixtures_path / "coupons.json", "w", encoding="utf-8") as f:
        json.dump(
            coupons_json,
            f,
            ensure_ascii=False,
            indent=2,
        )


if __name__ == "__main__":
    main()

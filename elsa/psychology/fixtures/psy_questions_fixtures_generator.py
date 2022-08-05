import json
import django
import gspread

from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from django.conf import settings

from configuration.settings.config_utils import get_env_variable

datetime_fields = {
    "created_at": str(datetime.now(timezone.utc)),
    "updated_at": str(datetime.now(timezone.utc)),
}


def parse_scale(data):
    parsed_data = []
    pks = []
    STRING_TO_SCALE = {
        "Totalmente Irracional": "TI",
        "Bastante Irracional": "VI",
        "Algo Irracional": "SI",
        "Algo Racional": "SR",
        "Bastante Racional": "VR",
        "Totalmente Racional": "TR",
    }

    for row in data:
        lower, value, upper = row
        pk = str(uuid4())
        pks.append(pk)
        parsed_data.append(
            {
                "model": "psychology.IrrationalBeliefScale",
                "pk": pk,
                "fields": {
                    "value": STRING_TO_SCALE[value.strip()],
                    "lower_limit": int(lower),
                    "upper_limit": int(upper),
                    **datetime_fields,
                },
            }
        )

    return parsed_data, pks


def parse_belief_week_data(tests_data, subquestions):
    data = []
    for test, subquestions in zip(tests_data, subquestions):
        parent_pk = str(uuid4())
        test_week, test_day, sum_desc, scales = test
        desc = (
            "A continuación se presentan una serie de ideas "
            + "acerca de diversos aspectos de la vida. Deberá indicar en qué "
            + "medida describen suforma de pensar habitual con la siguiente "
            + "clave de acuerdo:\nTD= Totalmente en desacuerdo\n"
            + "BD= Bastante en desacuerdo\n AD= Algo en desacuerdo AA= Algo "
            + "de acuerdo\nBA= Bastante de acuerdo\n TA= Totalmente de acuerdo"
        )
        data.append(
            {
                "model": "psychology.IrrationalBeliefQuestionaire",
                "pk": parent_pk,
                "fields": {
                    "day": test_day,
                    "week": test_week,
                    "title": "TEST DE CREENCIAS IRRACIONALES",
                    "description": desc,
                    "summary_description": sum_desc,
                    "summary_scales": scales,
                    **datetime_fields,
                },
            }
        )
        for day_data in subquestions:
            number, description = day_data[0].split(".", maxsplit=1)
            pk = str(uuid4())
            data.append(
                {
                    "model": "psychology.IrrationalBeliefQuestion",
                    "pk": pk,
                    "fields": {
                        "questionaire": parent_pk,
                        "number": int(number),
                        "description": description.strip().replace("\n", ""),
                        **datetime_fields,
                    },
                }
            )

    return data


def parse_inventory_week_data(
    week: int, inventory_summaries, subquestions, dayoffset: int = 0
):
    data = []
    for count, value in enumerate(zip(inventory_summaries, subquestions)):
        summary, subquestions = value
        parent_pk = str(uuid4())
        data.append(
            {
                "model": "psychology.PsychologicalInventoryQuestionaire",
                "pk": parent_pk,
                "fields": {
                    "day": count + dayoffset,
                    "week": week,
                    "title": "Inventario Psicológico de Ejecución "
                    + "Deportiva (IPED)",
                    "description": "A continuación encontrarás "
                    + "una serie de afirmaciones referidas a tus "
                    + "pensamientos, sentimientos, actitudes o "
                    + "comportamientos durante los entrenamientos "
                    + "y/o competencias o partidos. Lee atentamente "
                    + "cada frase y decide la frecuencia con la que "
                    + "crees que se produce cada una de ellas.",
                    "summary_description": summary,
                    **datetime_fields,
                },
            }
        )
        for day_data in subquestions:
            number, description = day_data[0].split(".", maxsplit=1)
            pk = str(uuid4())
            data.append(
                {
                    "model": "psychology.PsychologicalInventoryQuestion",
                    "pk": pk,
                    "fields": {
                        "questionaire": parent_pk,
                        "number": int(number),
                        "description": description.strip(),
                        **datetime_fields,
                    },
                }
            )

    return data


def main():
    django.setup()

    cred_path = Path.home() / get_env_variable("GOOGLE_CREDENTIALS_PATH")
    google_client = gspread.service_account(filename=str(cred_path))

    sheet = google_client.open_by_key(get_env_variable("GS_PSYCHOLOGY_ID"))
    worksheet = sheet.get_worksheet(0)

    # Tuples of (week, day, descriptio, is_subquestion)
    WEEK_1_QUESTIONS = [
        (
            1,
            1,
            "¿En qué medida eres capaz de controlar el nerviosismo antes, "
            + "durante y después de la competición o el entreno?\n(Responde "
            + "sabiendo que 0 es que te consideras poco capaz y 10 muy capaz)",
            False,
        ),
        (
            1,
            2,
            "¿Disfrutas compitiendo en tu deporte?\n(Responde sabiendo que "
            + "0 es que no disfrutas nada en tu deporte y 10 que disfrutas "
            + "muchísimo).",
            False,
        ),
        (
            1,
            3,
            "Puntúa de 0 a 10 en que medida prefieres competir contra...\n"
            + "(Responde sabiendo que 0 sería que no te gusta nada competir "
            + "contra ellos y 10 que te gusta muchísimo competir contra "
            + "ellos)",
            False,
        ),
        (1, 1, "Rivales teóricamente superiores.", True),
        (1, 2, "Rivales teóricamente inferiores.", True),
        (1, 3, " Rivales de parecido nivel al tuyo.", True),
        (
            1,
            4,
            "¿Te esfuerzas al máximo en los entrenamientos para poder "
            + "destacar en las pruebas?",
            False,
        ),
        (
            1,
            5,
            "¿En qué medida sales a entrenar/competir convencido de "
            + "que vas a hacerlo bien?\n(Responde sabiendo que 0 "
            + "es nada convencido y 10 es totalmente convencido)",
            False,
        ),
        (
            1,
            6,
            "Si tuvieras que ponerte una nota (de 0 a 10) en los "
            + "aspectos técnicos, tácticos, físicos y psicológicos "
            + "¿Cuál sería ésta?",
            False,
        ),
        (1, 1, "Aspecto técnico", True),
        (1, 2, "Aspecto físico", True),
        (1, 3, "Aspecto psicológico", True),
        (
            1,
            7,
            "¿En qué medida factores externos como público, "
            + "familiares, amigos, etc. suelen afectar a tu "
            + "rendimiento?\n(Responde sabiendo que 0 es que "
            + "no te afecta y 10 que te afecta mucho)",
            False,
        ),
        (
            2,
            8,
            "¿Practicas mentalmente las habilidades técnicas o "
            + "tácticas de tu deporte?",
            False,
        ),
        (
            2,
            9,
            "¿Intentas concentrarte antes de salir a entrenar/competir?",
            False,
        ),
        (
            2,
            10,
            "¿En qué medida sueles estar concentrado durante una rodada o "
            + "fondo?\n(Responde sabiendo que 0 es que no sueles "
            + "estar concentrado y 10 que sueles estarlo)",
            False,
        ),
        (
            2,
            11,
            "¿En qué medida eres capaz de controlar tus emociones "
            + "antes, durante y después de la competencia/entreno?\n"
            + "(Responde sabiendo que 0 es que te consideras poco "
            + "capaz y 10 muy capaz)",
            False,
        ),
        (
            2,
            12,
            "¿Cuáles son, desde el punto de vista técnico, tus puntos "
            + "fuertes y débiles?",
            False,
        ),
        (
            2,
            13,
            "¿Dime dos razones por orden de prioridad por las "
            + "que prácticas ciclismo?",
            False,
        ),
        (
            2,
            14,
            "¿Qué tal relación tienes con tus compañeros de entrenamiento?",
            False,
        ),
        (
            3,
            15,
            "Enlista en orden las cinco principales cosas que más te "
            + "causan estres o ansiedad a la hora de la practica del "
            + "ciclismo.",
            False,
        ),
        (
            4,
            16,
            "Que objetivos de realización o ejecución tienes? Enlizta tres",
            False,
        ),
    ]

    # Irrational Beliefs test parsing.
    scale1, scale2, scale3, scale4 = worksheet.batch_get(
        ["L125:N130", "L146:N151", "L166:N171", "L244:N249"]
    )
    scale_usage = {
        1: parse_scale(scale1),
        2: parse_scale(scale2),
        3: parse_scale(scale3),
        4: parse_scale(scale3),
        5: parse_scale(scale2),
        6: parse_scale(scale1),
        7: parse_scale(scale4),
        8: parse_scale(scale3),
        9: parse_scale(scale1),
        10: parse_scale(scale2),
    }
    json_data = []
    for key, value in scale_usage.items():
        json_data += value[0]

    summaries_descriptions = worksheet.batch_get(
        [
            "O125:W132",
            "O146:W153",
            "O166:W173",
            "O186:W193",
            "O205:W212",
            "O224:W232",
            "O244:W251",
            "O264:W271",
            "O283:W290",
            "O303:W310",
        ]
    )
    summaries_descriptions = [
        d for sublist in summaries_descriptions for d in sublist
    ]
    summaries_descriptions = [
        d.replace("\n", " ")
        for sublist in summaries_descriptions
        for d in sublist
    ]
    week1_summaries = []
    week2_summaries = []

    for count, value in enumerate(summaries_descriptions[:3]):
        week1_summaries.append(
            (1, count + 5, value, scale_usage[count + 1][1])
        )

    for count, value in enumerate(summaries_descriptions[3:]):
        week2_summaries.append(
            (2, count + 1, value, scale_usage[count + 4][1])
        )

    week1_day5, week1_day6, week1_day7 = worksheet.batch_get(
        ["D126:D132", "D147:D151", "D166:D171"]
    )
    week2 = worksheet.batch_get(
        [
            "D187:D192",
            "D206:D210",
            "D225:D231",
            "D245:D247",
            "D264:D269",
            "D284:D290",
            "D304:D308",
        ]
    )

    WEEK_3_QUESTIONS = [
        (
            1,
            "TECNICAMENTE (Ej: DEFECTO = Manejo de las relaciones o cambios "
            + "/ VIRTUD = Escalador)",
        ),
        (1, "FÍSICAMENTE (Ej: DEFECTO = Sobrepeso / VIRTUD = Rapido)"),
        (
            2,
            "PSICOLÓGICAMENTE (Ej: DEFECTO = Ansioso / VIRTUD = Pensamiento "
            + "positivo)",
        ),
        (
            2,
            "PERSONALMENTE (Ej: DEFECTO = Pereza / virtud = Comprometido)",
        ),
    ]

    (
        week3_day3,
        week3_day4,
        week3_day5,
        week3_day6,
        week3_day7,
    ) = worksheet.batch_get(
        ["D391:D396", "D406:D411", "D421:D426", "D436:D441", "D451:D456"]
    )

    week4_day1, week4_day2 = worksheet.batch_get(["D467:D472", "D482:D487"])

    questions_data = []
    for day, number, description, is_subquestion in WEEK_1_QUESTIONS:
        pk = str(uuid4())
        if not is_subquestion:
            parent_pk = pk

        data = {
            "uuid": pk,
            "day": day,
            "week": 1,
            "number": number,
            "description": description,
        }

        if is_subquestion:
            data["parent"] = parent_pk

        questions_data.append(data)

    for day, description in WEEK_3_QUESTIONS:
        pk = str(uuid4())
        data = {"uuid": pk, "day": day, "week": 3, "description": description}
        questions_data.append(data)

    # Irrational beliefs test
    belief_test_data = []
    belief_test_data += parse_belief_week_data(
        week1_summaries, [week1_day5, week1_day6, week1_day7]
    )
    belief_test_data += parse_belief_week_data(week2_summaries, week2)

    # Psychological inventory
    week3_summaries = [
        "Autoconfianza",
        "Control de afrontamiento negativo",
        "Control atencional",
        "Control visual-imaginativo",
        "Nivel motivacional",
    ]
    inventory_data = []
    inventory_data += parse_inventory_week_data(
        3,
        week3_summaries,
        [
            week3_day3,
            week3_day4,
            week3_day5,
            week3_day6,
            week3_day7,
        ],
        dayoffset=3,
    )
    week4_summaries = [
        "Control de afrontamiento positivo",
        "Control actitudinal",
    ]
    inventory_data += parse_inventory_week_data(
        4, week4_summaries, [week4_day1, week4_day2]
    )

    json_data += belief_test_data + inventory_data
    for entry in questions_data:
        pk = entry.pop("uuid")
        json_data.append(
            {
                "model": "psychology.PsychologicalQuestion",
                "pk": pk,
                "fields": {
                    **entry,
                    "created_at": str(datetime.now(timezone.utc)),
                    "updated_at": str(datetime.now(timezone.utc)),
                },
            }
        )

    json_file_path = (
        settings.BASE_DIR
        / "elsa"
        / "psychology"
        / "fixtures"
        / "psychological_questions.json"
    )
    with open(json_file_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()

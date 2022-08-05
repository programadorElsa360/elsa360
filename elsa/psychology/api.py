from django.db.models import Sum

from .models import MoodProfileAnswer


def get_feelings_sum(feelings):
    answers_qs = MoodProfileAnswer.objects.filter(feeling__in=feelings)

    sum = 0
    if answers_qs.exists():
        sum = answers_qs.aggregate(Sum("intensity"))["intensity__sum"]

    return sum

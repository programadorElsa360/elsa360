from django.urls import path

from rest_framework import routers

from . import views
from . import viewsets


router = routers.SimpleRouter()
router.register(
    "psychology-plan-summaries",
    viewsets.PsychologicalSummaryViewSet,
    basename="psychology_plan_summaries",
)
router.register(
    "psychology-questions",
    viewsets.PsychologicalQuestionViewSet,
    basename="psychology_questions",
)
router.register(
    "psychology-answers",
    viewsets.PsychologicalQuestionAnswerViewset,
    basename="psychology_answers",
)
router.register(
    "psychology-beliefs-questionaires",
    viewsets.IrrationalBeliefsQuestionaireViewSet,
    basename="psychology_beliefs_questionaires",
)
router.register(
    "psychology-beliefs-summaries",
    viewsets.IrrationalBeliefsSummaryViewSet,
    basename="psychology_beliefs_summaries",
)
router.register(
    "psychology-beliefs-answers",
    viewsets.IrrationalBeliefsAnswerViewSet,
    basename="psychology_beliefs_answers",
)
router.register(
    "psychology-inventory-questionaires",
    viewsets.PsychologicalInventoryQuestionaireViewSet,
    basename="psychology_inventory_questionaires",
)
router.register(
    "psychology-inventory-summaries",
    viewsets.PsychologicalInventorySummaryViewSet,
    basename="psychology_inventory_summaries",
)
router.register(
    "psychology-inventory-answers",
    viewsets.PsychologicalInventoryAnswerViewSet,
    basename="psychology_inventory_answers",
)
router.register(
    "psychology-borgh-summaries",
    viewsets.BorghSummaryViewSet,
    basename="psychology_borgh_summaries",
)
router.register(
    "psychology-hamilton-summaries",
    viewsets.HamiltonSummaryViewSet,
    basename="psychology_hamilton_summaries",
)
router.register(
    "psychology-hamilton-answers",
    viewsets.HamiltonQuestionAnswerViewSet,
    basename="psychology_hamilton_answers",
)
router.register(
    "psychology-mood-summaries",
    viewsets.MoodProfileSummaryViewSet,
    basename="psychology_mood_summaries",
)
router.register(
    "psychology-mood-answers",
    viewsets.MoodProfileAnswerViewSet,
    basename="psychology_mood_answers",
)

urlpatterns = [
    path(
        "psychology/daily/",
        views.DailyPsychologicalPlanView.as_view(),
        name="psychology_daily",
    ),
    path(
        "psychology/techniques/",
        views.PsychologicalTechniqueListView.as_view(),
        name="psychology_techniques",
    ),
    path(
        "psychology/borgh/",
        views.BorghScaleView.as_view(),
        name="psychology_borgh",
    ),
    path(
        "psychology/hamilton/",
        views.HamiltonQuestionView.as_view(),
        name="psychology_borgh",
    ),
    path(
        "psychology/mood-feelings/",
        views.MoodFeelingsListView.as_view(),
        name="psychology_feelings",
    ),
]
urlpatterns += router.urls

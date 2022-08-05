from knox.auth import TokenAuthentication

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from elsa.commons.authentication import IsAdminOrHasMembership

from .models import (
    BorghEffortScale,
    HamiltonQuestion,
    IrrationalBeliefQuestionaire,
    MoodProfileAnswer,
    PsychologicalInventoryQuestionaire,
    PsychologicalQuestion,
    PsychologicalTechnique,
)
from .serializers import (
    BorghEfforScaleSerializer,
    HamiltonQuestionSerializer,
    IrrationalBeliefQuestionaireSerializer,
    PsychologicalInventoryQuestionaireSerializer,
    PsychologicalQuestionSerializer,
    PsychologicalTechniqueSerializer,
)


# Create your views here.
class DailyPsychologicalPlanView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrHasMembership]

    def get(self, request):
        user = request.user

        current_day = user.current_training_day["relative"]
        current_week = user.current_training_week["relative"]

        questions_qs = PsychologicalQuestion.objects.filter(
            day=current_day, week=current_week
        )
        beliefs_qs = IrrationalBeliefQuestionaire.objects.filter(
            day=current_day, week=current_week
        ).first()
        inventory_qs = PsychologicalInventoryQuestionaire.objects.filter(
            day=current_day, week=current_week
        )

        borgh_qs = BorghEffortScale.objects.all()

        psy_techniques = [
            technique
            for technique in list(PsychologicalTechnique.objects.all())
            if technique.display_today(current_week, current_day)
        ]

        questions_serializer = PsychologicalQuestionSerializer(
            questions_qs, many=True
        )
        beliefs_serializer = IrrationalBeliefQuestionaireSerializer(beliefs_qs)
        inventory_serializer = PsychologicalInventoryQuestionaireSerializer(
            inventory_qs, many=True
        )
        borgh_serializer = BorghEfforScaleSerializer(borgh_qs, many=True)
        techniques_serializer = PsychologicalTechniqueSerializer(
            psy_techniques, many=True
        )

        mood_states = []
        mood_states_display_days = [(2, 1), (3, 2), (4, 1), (5, 1)]
        if (current_week, current_day) in mood_states_display_days:
            mood_states = MoodProfileAnswer.Feelings.choices

        hamilton_qs = []
        hamilton_display_days = [(2, 2), (3, 1), (4, 2), (5, 2)]
        if (current_week, current_day) in hamilton_display_days:
            hamilton_qs = HamiltonQuestion.objects.all()

        hamilton_serializer = HamiltonQuestionSerializer(
            hamilton_qs, many=True
        )

        return Response(
            {
                "regular_questions": questions_serializer.data,
                "beliefs_questionaire": beliefs_serializer.data,
                "psy_inventory": inventory_serializer.data,
                "borgh_scale": borgh_serializer.data,
                "techniques": techniques_serializer.data,
                "mood_states": mood_states,
                "hamilton": hamilton_serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class BorghScaleView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = BorghEffortScale.objects.all()
    serializer_class = BorghEfforScaleSerializer


class HamiltonQuestionView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = HamiltonQuestion.objects.all()
    serializer_class = HamiltonQuestionSerializer


class PsychologicalTechniqueListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PsychologicalTechnique.objects.all()
    serializer_class = PsychologicalTechniqueSerializer


class MoodFeelingsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            [
                {"enum": feeling.value, "label": feeling.label}
                for feeling in MoodProfileAnswer.Feelings
            ],
            status=status.HTTP_200_OK,
        )

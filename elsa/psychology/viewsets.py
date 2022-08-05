from elsa.commons.authentication import IsAdminOrHasMembership
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import (
    BorghSummary,
    HamiltonQuestionAnswer,
    HamiltonSummary,
    IrrationalBeliefAnswer,
    IrrationalBeliefQuestionaire,
    IrrationalBeliefSummary,
    MoodProfileAnswer,
    MoodProfileSummary,
    PsychologicalInventoryAnswer,
    PsychologicalInventoryQuestionaire,
    PsychologicalInventorySummary,
    PsychologicalPlanSummary,
    PsychologicalQuestion,
    PsychologicalQuestionAnswer,
)
from .serializers import (
    BorghSummarySerializer,
    HamiltonQuestionAnswerSerializer,
    HamiltonSummarySerializer,
    IrrationalBeliefAnswerSerializer,
    IrrationalBeliefQuestionaireSerializer,
    IrrationalBeliefSummarySerializer,
    MoodProfileAnswerSerializer,
    MoodProfileSummarySerializer,
    PsychologicalInventoryAnswerSerializer,
    PsychologicalInventoryQuestionaireSerializer,
    PsychologicalInventorySummarySerializer,
    PsychologicalQuestionAnswerSerializer,
    PsychologicalQuestionSerializer,
    PsychologicalSummarySerializer,
)


class PsychologicalSummaryViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrHasMembership]
    serializer_class = PsychologicalSummarySerializer

    def get_queryset(self):
        if self.request is None:
            return PsychologicalPlanSummary.objects.none()

        if self.request.user.is_staff:
            return PsychologicalPlanSummary.objects.all()
        else:
            return PsychologicalPlanSummary.objects.filter(
                user=self.request.user.pk
            )


class PsychologicalQuestionViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrHasMembership]
    queryset = PsychologicalQuestion.objects.all()
    serializer_class = PsychologicalQuestionSerializer


class PsychologicalQuestionAnswerViewset(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrHasMembership]
    serializer_class = PsychologicalQuestionAnswerSerializer

    def get_queryset(self):
        if self.request is None:
            return PsychologicalQuestionAnswer.objects.none()

        if self.request.user.is_staff:
            return PsychologicalQuestionAnswer.objects.all()
        else:
            return PsychologicalQuestionAnswer.objects.filter(
                summary__user=self.request.user.pk
            )

    @action(detail=False, methods=["post"], url_path="batch-create")
    def batch_create(self, request):
        serializer = self.serializer_class(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class IrrationalBeliefsQuestionaireViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = IrrationalBeliefQuestionaire.objects.all()
    serializer_class = IrrationalBeliefQuestionaireSerializer


class IrrationalBeliefsSummaryViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrHasMembership]
    serializer_class = IrrationalBeliefSummarySerializer

    def get_queryset(self):
        if self.request is None:
            return IrrationalBeliefSummary.objects.none()

        if self.request.user.is_staff:
            return IrrationalBeliefSummary.objects.all()
        else:
            return IrrationalBeliefSummary.objects.filter(
                user=self.request.user.pk
            )


class IrrationalBeliefsAnswerViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrHasMembership]
    serializer_class = IrrationalBeliefAnswerSerializer

    def get_queryset(self):
        if self.request is None:
            return IrrationalBeliefAnswer.objects.none()

        if self.request.user.is_staff:
            return IrrationalBeliefAnswer.objects.all()
        else:
            return IrrationalBeliefAnswer.objects.filter(
                summary__user=self.request.user.pk
            )


class PsychologicalInventoryQuestionaireViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = PsychologicalInventoryQuestionaire.objects.all()
    serializer_class = PsychologicalInventoryQuestionaireSerializer


class PsychologicalInventorySummaryViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrHasMembership]
    serializer_class = PsychologicalInventorySummarySerializer

    def get_queryset(self):
        if self.request is None:
            return PsychologicalInventorySummary.objects.none()

        if self.request.user.is_staff:
            return PsychologicalInventorySummary.objects.all()
        else:
            return PsychologicalInventorySummary.objects.filter(
                user=self.request.user.pk
            )


class PsychologicalInventoryAnswerViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrHasMembership]
    serializer_class = PsychologicalInventoryAnswerSerializer

    def get_queryset(self):
        if self.request is None:
            return PsychologicalInventoryAnswer.objects.none()

        if self.request.user.is_staff:
            return PsychologicalInventoryAnswer.objects.all()
        else:
            return PsychologicalInventoryAnswer.objects.filter(
                summary__user=self.request.user.pk
            )


class BorghSummaryViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrHasMembership]
    serializer_class = BorghSummarySerializer

    def get_queryset(self):
        if self.request is None:
            return BorghSummary.objects.none()

        if self.request.user.is_staff:
            return BorghSummary.objects.all()
        else:
            return BorghSummary.objects.filter(user=self.request.user.pk)


class HamiltonSummaryViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrHasMembership]
    serializer_class = HamiltonSummarySerializer

    def get_queryset(self):
        if self.request is None:
            return HamiltonSummary.objects.all()

        if self.request.user.is_staff:
            return HamiltonSummary.objects.all()
        else:
            return HamiltonSummary.objects.filter(user=self.request.user.pk)


class HamiltonQuestionAnswerViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrHasMembership]
    serializer_class = HamiltonQuestionAnswerSerializer

    def get_queryset(self):
        if self.request is None:
            return HamiltonQuestionAnswer.objects.none()

        if self.request.user.is_staff:
            return HamiltonQuestionAnswer.objects.all()
        else:
            return HamiltonQuestionAnswer.objects.filter(
                summary__user=self.request.user.pk
            )


class MoodProfileSummaryViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrHasMembership]
    serializer_class = MoodProfileSummarySerializer

    def get_queryset(self):
        if self.request is None:
            return MoodProfileAnswer.objects.none()

        if self.request.user.is_staff:
            return MoodProfileSummary.objects.all()
        else:
            return MoodProfileSummary.objects.filter(user=self.request.user.pk)


class MoodProfileAnswerViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrHasMembership]
    serializer_class = MoodProfileAnswerSerializer

    def get_queryset(self):
        if self.request is None:
            return MoodProfileAnswer.objects.none()

        if self.request.user.is_staff:
            return MoodProfileAnswer.objects.all()
        else:
            return MoodProfileAnswer.objects.filter(
                summary__user=self.request.user.pk
            )

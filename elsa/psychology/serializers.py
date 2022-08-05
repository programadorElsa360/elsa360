from django.db.models import Sum, Q
from elsa.commons.enums import HAMILTON_ANXIETY_SCORE
from rest_framework import serializers

from .api import get_feelings_sum
from .models import (
    BorghEffortScale,
    BorghSummary,
    HamiltonQuestion,
    HamiltonQuestionAnswer,
    HamiltonSummary,
    IrrationalBeliefAnswer,
    IrrationalBeliefQuestionaire,
    IrrationalBeliefSummary,
    PsychologicalInventoryQuestionaire,
    PsychologicalInventorySummary,
    PsychologicalInventoryAnswer,
    MoodProfileAnswer,
    MoodProfileSummary,
    PsychologicalPlanSummary,
    PsychologicalQuestion,
    PsychologicalTechnique,
    PsychologicalQuestionAnswer,
)


class PsychologicalSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = PsychologicalPlanSummary
        fields = ["pk", "user", "start_date", "end_date"]


class PsychologicalQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PsychologicalQuestion
        fields = ["pk", "day", "week", "number", "description", "parent"]


class PsychologicalQuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PsychologicalQuestionAnswer
        fields = [
            "question",
            "answer_subject",
            "string_answer",
            "boolean_answer",
            "intensity_answer",
            "integer_scale_answer",
            "qualificative_answer",
        ]


class IrrationalBeliefQuestionaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = IrrationalBeliefQuestionaire
        fields = [
            "pk",
            "day",
            "week",
            "title",
            "description",
            "summary_description",
            "summary_scales",
            "questions",
        ]
        depth = 1


class IrrationalBeliefSummarySerializer(serializers.ModelSerializer):
    score = serializers.SerializerMethodField()
    result = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = IrrationalBeliefSummary
        fields = [
            "pk",
            "user",
            "questionaire",
            "description",
            "answers",
            "score",
            "result",
        ]

    def get_score(self, obj):
        score = obj.answers.aggregate(Sum("intensity"))["intensity__sum"]
        return 0 if score is None else score

    def get_result(self, obj):
        score = self.get_score(obj)
        scale = obj.questionaire.summary_scales.filter(
            Q(lower_limit__lte=score) & Q(upper_limit__gte=score)
        ).first()
        return None if scale is None else scale.get_value_display()

    def get_description(self, obj):
        return obj.questionaire.summary_description


class IrrationalBeliefAnswerSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        answer = "answer" in attrs
        intensity = "intensity" in attrs

        if (answer and not intensity) or (not answer and intensity):
            raise serializers.ValidationError(
                "'answer' and 'intensity' " + "fields must be sent together"
            )

        return attrs

    class Meta:
        model = IrrationalBeliefAnswer
        fields = ["summary", "answer", "intensity"]


class PsychologicalInventoryQuestionaireSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = PsychologicalInventoryQuestionaire
        fields = [
            "pk",
            "day",
            "week",
            "title",
            "description",
            "summary_description",
            "questions",
        ]
        depth = 1


class PsychologicalInventorySummarySerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()

    class Meta:
        model = PsychologicalInventorySummary
        fields = ["pk", "user", "questionaire", "description", "score"]

    def get_description(self, obj):
        return obj.questionaire.summary_description

    def get_score(self, obj):
        return obj.answers.aggregate(Sum("answer"))["answer__sum"]


class PsychologicalInventoryAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PsychologicalInventoryAnswer
        fields = ["pk", "summary", "answer"]


class BorghEfforScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorghEffortScale
        fields = ["pk", "description", "intensity", "lower_rpe", "higher_rpe"]


class BorghSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = BorghSummary
        fields = ["pk", "user", "answer", "created_at"]


class HamiltonQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HamiltonQuestion
        fields = ["pk", "number", "title", "description"]


class HamiltonQuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HamiltonQuestionAnswer
        fields = ["pk", "summary", "question", "answer"]


class HamiltonSummarySerializer(serializers.ModelSerializer):
    score = serializers.SerializerMethodField()
    result = serializers.SerializerMethodField()

    class Meta:
        model = HamiltonSummary
        fields = ["pk", "user", "answers", "score", "result"]

    def get_score(self, obj):
        return obj.answers.all().aggregate(Sum("answer"))["answer__sum"]

    def get_result(self, obj):
        for key, value in HAMILTON_ANXIETY_SCORE.items():
            if self.get_score(obj) in range(key[0], key[1] + 1):
                return value

        return None


class MoodProfileSummarySerializer(serializers.ModelSerializer):
    fatigue = serializers.SerializerMethodField()
    confusion = serializers.SerializerMethodField()
    vigor = serializers.SerializerMethodField()
    depression = serializers.SerializerMethodField()
    anger = serializers.SerializerMethodField()
    tension = serializers.SerializerMethodField()
    general_mood = serializers.SerializerMethodField()

    class Meta:
        model = MoodProfileSummary
        fields = [
            "pk",
            "user",
            "fatigue",
            "confusion",
            "vigor",
            "depression",
            "anger",
            "tension",
            "general_mood",
        ]

    def get_fatigue(self, obj):
        feelings = [
            MoodProfileAnswer.Feelings.WORN,
            MoodProfileAnswer.Feelings.APATHETIC,
            MoodProfileAnswer.Feelings.FATIGUED,
            MoodProfileAnswer.Feelings.EXHAUSTED,
            MoodProfileAnswer.Feelings.SLOW,
            MoodProfileAnswer.Feelings.TIRED,
            MoodProfileAnswer.Feelings.DRAINED,
        ]
        return get_feelings_sum(feelings)

    def get_confusion(self, obj):
        feelings = [
            MoodProfileAnswer.Feelings.CONFUSED,
            MoodProfileAnswer.Feelings.UNABLE_TO_CONCENTRATE,
            MoodProfileAnswer.Feelings.CONFUSING,
            MoodProfileAnswer.Feelings.BEWILDERED,
            MoodProfileAnswer.Feelings.EFFICIENT,
            MoodProfileAnswer.Feelings.FORGETFUL,
            MoodProfileAnswer.Feelings.UNCERTAIN,
        ]
        return get_feelings_sum(feelings)

    def get_vigor(self, obj):
        # TODO add "Lleno de pep" enum.
        feelings = [
            MoodProfileAnswer.Feelings.DYNAMIC,
            MoodProfileAnswer.Feelings.ACTIVE,
            MoodProfileAnswer.Feelings.ENERGETIC,
            MoodProfileAnswer.Feelings.HAPPY,
            MoodProfileAnswer.Feelings.ALERT,
            MoodProfileAnswer.Feelings.CAREFREE,
            MoodProfileAnswer.Feelings.CHEERFUL,
            MoodProfileAnswer.Feelings.VIGOROUS,
        ]
        return get_feelings_sum(feelings)

    def get_depression(self, obj):
        feelings = [
            MoodProfileAnswer.Feelings.UNHAPPY,
            MoodProfileAnswer.Feelings.SORRY,
            MoodProfileAnswer.Feelings.SAD,
            MoodProfileAnswer.Feelings.BLUE,
            MoodProfileAnswer.Feelings.HOPELESS,
            MoodProfileAnswer.Feelings.UNWORTHY,
            MoodProfileAnswer.Feelings.DISCOURAGED,
            MoodProfileAnswer.Feelings.ALONE,
            MoodProfileAnswer.Feelings.MISERABLE,
            MoodProfileAnswer.Feelings.SOMBER,
            MoodProfileAnswer.Feelings.DESPERATE,
            MoodProfileAnswer.Feelings.DEFENSELESS,
            MoodProfileAnswer.Feelings.WORTHLESS,
            MoodProfileAnswer.Feelings.TERRIFIED,
            MoodProfileAnswer.Feelings.GUILTY,
        ]
        return get_feelings_sum(feelings)

    def get_anger(self, obj):
        feelings = [
            MoodProfileAnswer.Feelings.ANGRY,
            MoodProfileAnswer.Feelings.FURIOUS,
            MoodProfileAnswer.Feelings.GRUMPY,
            MoodProfileAnswer.Feelings.MALICIOUS,
            MoodProfileAnswer.Feelings.UPSET,
            MoodProfileAnswer.Feelings.RESENTFUL,
            MoodProfileAnswer.Feelings.BITTER,
            MoodProfileAnswer.Feelings.FIGHT_READY,
            MoodProfileAnswer.Feelings.REBELLIOUS,
            MoodProfileAnswer.Feelings.CHEATED,
            MoodProfileAnswer.Feelings.BAD_MOOD,
        ]
        return get_feelings_sum(feelings)

    def get_tension(self, obj):
        feelings = [
            MoodProfileAnswer.Feelings.TENSE,
            MoodProfileAnswer.Feelings.TREMBLING,
            MoodProfileAnswer.Feelings.NERVOUS,
            MoodProfileAnswer.Feelings.PANICKED,
            MoodProfileAnswer.Feelings.RELAXED,
            MoodProfileAnswer.Feelings.HARD_TO_HANDLE,
            MoodProfileAnswer.Feelings.RESTLESS,
            MoodProfileAnswer.Feelings.ANXIOUS,
        ]
        return get_feelings_sum(feelings)

    def get_general_mood(self, obj):
        return (
            self.get_tension(obj)
            + self.get_anger(obj)
            + self.get_fatigue(obj)
            + self.get_depression(obj)
            + self.get_confusion(obj)
        ) - self.get_vigor(obj)


class MoodProfileAnswerSerializer(serializers.ModelSerializer):
    feeling_label = serializers.SerializerMethodField()

    class Meta:
        model = MoodProfileAnswer
        fields = ["pk", "summary", "feeling", "feeling_label", "intensity"]

    def get_feeling_label(self, obj):
        return obj.get_feeling_display()


class PsychologicalTechniqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = PsychologicalTechnique
        fields = ["type", "title", "description"]

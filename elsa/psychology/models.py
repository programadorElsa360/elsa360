from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from elsa.commons.models import UUIDPrimaryKeyModel, TimeStampedModel
from elsa.commons.enums import WeekDays


# Create your models here.
class PsychologicalQuestion(UUIDPrimaryKeyModel, TimeStampedModel):
    """Represents a regular question."""

    day = models.IntegerField(
        choices=WeekDays.choices, default=WeekDays.MONDAY
    )
    week = models.IntegerField()
    number = models.IntegerField(null=True, blank=True)
    description = models.TextField()
    parent = models.ForeignKey(
        to="self", on_delete=models.SET_NULL, null=True, blank=True
    )


class PsychologicalPlanSummary(UUIDPrimaryKeyModel, TimeStampedModel):
    """Represents a psychological plan's period of activity."""

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    active = models.BooleanField(default=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class PsychologicalQuestionAnswer(UUIDPrimaryKeyModel, TimeStampedModel):
    """Represents an answer for a regular question."""

    class IntensityAnswers(models.IntegerChoices):
        NEVER = 0, _("Never")
        A_LITTLE = 1, _("A little")
        MODERATE = 2, _("Moderate")
        VERY_MUCH = 3, _("Very much")
        ALOT = 4, _("Alot")

    class QualificativeAnswers(models.IntegerChoices):
        VERY_GOOD = 0, _("Very good")
        GOOD = 1, _("Good")
        NORMAL = 2, _("Normal")
        REGULAR = 3, _("Regular")
        BAD = 4, _("Bad")

    question = models.ForeignKey(
        to=PsychologicalQuestion, on_delete=models.CASCADE
    )
    answer_subject = models.CharField(max_length=50, null=True, blank=True)
    string_answer = models.TextField(null=True, blank=True)
    boolean_answer = models.BooleanField(null=True, blank=True)
    intensity_answer = models.IntegerField(
        choices=IntensityAnswers.choices, null=True, blank=True
    )
    integer_scale_answer = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        null=True,
        blank=True,
    )
    qualificative_answer = models.IntegerField(
        choices=QualificativeAnswers.choices,
        null=True,
        blank=True,
    )


class IrrationalBeliefScale(UUIDPrimaryKeyModel, TimeStampedModel):
    class Scale(models.TextChoices):
        TOTALLY_IRRATIONAL = "TI", _("Totally irrational")
        VERY_IRRATIONAL = "VI", _("Very irrational")
        SOMEWHAT_IRRATIONAL = "SI", _("Somewhat irrational")
        SOMEWHAT_RATIONAL = "SR", _("Somewhat rational")
        VERY_RATIONAL = "VR", _("Very rational")
        TOTALLY_RATIONAL = "TR", _("Totally rational")

    value = models.CharField(
        max_length=2, choices=Scale.choices, default=Scale.SOMEWHAT_RATIONAL
    )
    lower_limit = models.IntegerField(
        validators=[MinValueValidator(3), MaxValueValidator(42)]
    )
    upper_limit = models.IntegerField(
        validators=[MinValueValidator(3), MaxValueValidator(42)]
    )


class IrrationalBeliefQuestionaire(UUIDPrimaryKeyModel, TimeStampedModel):
    day = models.IntegerField(
        choices=WeekDays.choices, default=WeekDays.MONDAY
    )
    week = models.IntegerField()
    title = models.CharField(max_length=30)
    description = models.TextField()
    summary_description = models.TextField()
    summary_scales = models.ManyToManyField(to=IrrationalBeliefScale)


class IrrationalBeliefQuestion(UUIDPrimaryKeyModel, TimeStampedModel):
    questionaire = models.ForeignKey(
        to=IrrationalBeliefQuestionaire,
        related_name="questions",
        on_delete=models.CASCADE,
    )
    number = models.IntegerField()
    description = models.CharField(max_length=140)


class IrrationalBeliefSummary(UUIDPrimaryKeyModel, TimeStampedModel):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    questionaire = models.ForeignKey(
        to=IrrationalBeliefQuestionaire,
        related_name="summaries",
        on_delete=models.CASCADE,
    )


class IrrationalBeliefAnswer(UUIDPrimaryKeyModel, TimeStampedModel):
    class Answers(models.TextChoices):
        TOTAL_DISAGREEMENT = "TD", _("Total disagreement")
        MUCH_DISAGREEMENT = "MD", _("Much disagreement")
        SOME_DISAGREEMENT = "SD", _("Some disagreement")
        SOME_AGREEMENT = "SA", _("Some agreement")
        MUCH_AGREEMENT = "MA", _("Much agreement")
        TOTAL_AGREEMENT = "TA", _("Total agreement")

    summary = models.ForeignKey(
        to=IrrationalBeliefSummary,
        related_name="answers",
        on_delete=models.CASCADE,
    )
    answer = models.CharField(max_length=2, choices=Answers.choices)
    intensity = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(6)]
    )


class PsychologicalInventoryQuestionaire(
    UUIDPrimaryKeyModel, TimeStampedModel
):
    day = models.IntegerField(
        choices=WeekDays.choices, default=WeekDays.MONDAY
    )
    week = models.IntegerField()
    title = models.CharField(max_length=52)
    description = models.TextField()
    summary_description = models.TextField()


class PsychologicalInventoryQuestion(UUIDPrimaryKeyModel, TimeStampedModel):
    questionaire = models.ForeignKey(
        to=PsychologicalInventoryQuestionaire,
        related_name="questions",
        on_delete=models.CASCADE,
    )
    number = models.IntegerField()
    description = models.CharField(max_length=152)


class PsychologicalInventorySummary(UUIDPrimaryKeyModel, TimeStampedModel):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    questionaire = models.ForeignKey(
        to=PsychologicalInventoryQuestionaire,
        related_name="summaries",
        on_delete=models.CASCADE,
    )


class PsychologicalInventoryAnswer(UUIDPrimaryKeyModel, TimeStampedModel):
    class Answers(models.IntegerChoices):
        ALMOST_ALWAYS = 5, _("Almost always")
        MANY_TIMES = 4, _("Many times")
        SOMETIMES = 3, _("Sometimes")
        FEW_TIMES = 2, _("A few times")
        ALMOST_NEVER = 1, _("Almost never")

    summary = models.ForeignKey(
        to=PsychologicalInventorySummary,
        related_name="answers",
        on_delete=models.CASCADE,
    )
    answer = models.IntegerField(
        choices=Answers.choices, default=Answers.SOMETIMES
    )


class BorghEffortScale(UUIDPrimaryKeyModel, TimeStampedModel):
    class BorghScale(models.TextChoices):
        EXTREMELY_SOFT = "E_S", _("Very, very soft")
        VERY_SOFT = "V_S", _("Very soft")
        SOFT = "S", _("Soft")
        SOMEWHAT_HARD = "S_H", _("Somewhat hard")
        HARD = "H", _("Hard")
        EXTREMELY_HARD = "E_H", _("Very, very hard")

    description = models.CharField(max_length=112)
    intensity = models.CharField(
        max_length=3, choices=BorghScale.choices, default=BorghScale.SOFT
    )
    lower_rpe = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    higher_rpe = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )


class BorghSummary(UUIDPrimaryKeyModel, TimeStampedModel):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    answer = models.ForeignKey(to=BorghEffortScale, on_delete=models.CASCADE)


class HamiltonQuestion(UUIDPrimaryKeyModel, TimeStampedModel):
    number = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(14)]
    )
    title = models.CharField(max_length=55)
    description = models.TextField()


class HamiltonSummary(UUIDPrimaryKeyModel, TimeStampedModel):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )


class HamiltonQuestionAnswer(UUIDPrimaryKeyModel, TimeStampedModel):
    class HamiltonScale(models.IntegerChoices):
        ABSENT = 0, _("Absent")
        MILD = 1, _("Mild")
        MODERATE = 2, _("Moderate")
        GRAVE = 3, _("Grave")
        INCAPACITATING = 4, _("Incapacitating")

    question = models.ForeignKey(to=HamiltonQuestion, on_delete=models.CASCADE)
    answer = models.IntegerField(
        choices=HamiltonScale.choices,
        default=HamiltonScale.ABSENT,
    )
    summary = models.ForeignKey(
        to=HamiltonSummary, related_name="answers", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ["question", "summary"]


class MoodProfileSummary(UUIDPrimaryKeyModel, TimeStampedModel):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )


class MoodProfileAnswer(UUIDPrimaryKeyModel, TimeStampedModel):
    class Feelings(models.TextChoices):
        FRIENDLY = "FD", _("Friendly")
        TENSE = "TE", _("Tense")
        ANGRY = "AN", _("Angry")
        WORN = "WR", _("Worn")
        UNHAPPY = "UH", _("Unhappy")
        HOT_HEADED = "HH", _("Hot headed")
        DYNAMIC = "DY", _("Dynamic")
        CONFUSED = "CF", _("Confused")
        SORRY = "SR", _("Sorry")
        TREMBLING = "TR", _("Trembling")
        APATHETIC = "AP", _("Apathetic")
        FURIOUS = "FU", _("Furious")
        CONSIDERED = "CN", _("Considered")
        SAD = "SA", _("Sad")
        ACTIVE = "AC", _("Active")
        NERVOUS = "NR", _("Nervous")
        GRUMPY = "GR", _("Grumpy")
        BLUE = "BL", _("Blue")
        ENERGETIC = "EN", _("Energetic")
        PANICKED = "PA", _("Panicked")
        HOPELESS = "HL", _("Hopeless")
        RELAXED = "RE", _("Relaxed")
        UNWORTHY = "UW", _("Unworthy")
        MALICIOUS = "ML", _("Malicious")
        SYMPATHETIC = "SP", _("Sympathetic")
        HARD_TO_HANDLE = "HT", _("Hard to handle")
        RESTLESS = "RT", _("Restless")
        UNABLE_TO_CONCENTRATE = "UC", _("Unable to concentrate")
        FATIGUED = "FA", _("Fatigued")
        USEFUL = "US", _("Useful")
        UPSET = "UP", _("Upset")
        DISCOURAGED = "DC", _("Discouraged")
        RESENTFUL = "RS", _("Resentful")
        ALONE = "AL", _("Alone")
        MISERABLE = "MS", _("Miserable")
        CONFUSING = "CO", _("Confusing")
        HAPPY = "HA", _("Happy")
        BITTER = "BI", _("Bitter")
        EXHAUSTED = "EX", _("Exhausted")
        ANXIOUS = "AX", _("Anxious")
        FIGHT_READY = "FR", _("Fight-ready")
        GOOD_MOOD = "GM", _("Good mood")
        SOMBER = "SO", _("Somber")
        DESPERATE = "DE", _("Desperate")
        SLOW = "SL", _("Slow")
        REBELLIOUS = "RB", _("Rebellious")
        DEFENSELESS = "DL", _("Defenseless")
        TIRED = "TI", _("Tired")
        BEWILDERED = "BW", _("Bewildered")
        ALERT = "AT", _("Alert")
        CHEATED = "CH", _("Cheated")
        EFFICIENT = "EF", _("Efficient")
        TRUSTWORTHY = "TW", _("Trustworthy")
        CHEERFUL = "CR", _("Full of pep")
        BAD_MOOD = "BM", _("Bad mood")
        WORTHLESS = "WL", _("Worthless")
        FORGETFUL = "FG", _("Forgetful")
        CAREFREE = "CA", _("Carefree")
        TERRIFIED = "TF", _("Terrified")
        GUILTY = "GT", _("Guilty")
        VIGOROUS = "VG", _("Vigorous")
        UNCERTAIN = "UN", _("Uncertain")
        DRAINED = "DR", _("Drained")

    class IntensityAnswers(models.IntegerChoices):
        NEVER = 0, _("Never")
        A_LITTLE = 1, _("A little")
        MODERATE = 2, _("Moderate")
        VERY_MUCH = 3, _("Very much")
        ALOT = 4, _("Alot")

    summary = models.ForeignKey(
        to=MoodProfileSummary, related_name="answers", on_delete=models.CASCADE
    )
    feeling = models.CharField(
        max_length=2, choices=Feelings.choices, default=Feelings.FRIENDLY
    )
    intensity = models.IntegerField(
        choices=IntensityAnswers.choices, default=IntensityAnswers.MODERATE
    )

    @property
    def norm_intensity(self):
        if self.feeling in [self.Feelings.EFFICIENT, self.Feelings.RELAXED]:
            return 4 - self.intensity
        else:
            return self.intensity


class PsychologicalTechnique(UUIDPrimaryKeyModel, TimeStampedModel):
    class Types(models.TextChoices):
        RESPIRATION = "RE", _("Respiration")
        JACOBSON = "JA", _("Jacobson")
        SCHULTZ = "SZ", _("Schultz")
        HAYNES = "HA", _("Schwartz & Haynes")
        VISUALIZATION = "VI", _("Visualization")

    type = models.CharField(
        max_length=2,
        choices=Types.choices,
        default=Types.RESPIRATION,
    )
    title = models.CharField(max_length=55)
    description = models.TextField()

    def display_today(self, week, day):
        # dict of [key: TechniqueType] : [(week: int, day: int)]
        DISPLAY_DAYS = {
            self.Types.RESPIRATION: [
                (1, 3),
                (2, 6),
                (3, 3),
                (4, 6),
                (5, 6),
            ],
            self.Types.JACOBSON: [
                (1, 4),
                (2, 3),
                (3, 5),
                (4, 3),
                (5, 3),
            ],
            self.Types.SCHULTZ: [
                (1, 6),
                (2, 5),
                (3, 7),
                (4, 5),
                (5, 5),
            ],
            self.Types.HAYNES: [
                (1, 7),
                (2, 7),
                (3, 4),
                (4, 7),
                (5, 7),
            ],
            self.Types.VISUALIZATION: [
                (1, 5),
                (2, 4),
                (3, 6),
                (4, 4),
                (5, 4),
            ],
        }

        return (week, day) in DISPLAY_DAYS[self.type]

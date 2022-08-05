from django.contrib import admin

import elsa.psychology.models as models

# Register your models here.
admin.site.register(
    [
        models.PsychologicalPlanSummary,
        models.PsychologicalQuestion,
        models.PsychologicalQuestionAnswer,
        models.IrrationalBeliefScale,
        models.IrrationalBeliefSummary,
        models.IrrationalBeliefQuestion,
        models.IrrationalBeliefAnswer,
        models.PsychologicalInventoryQuestionaire,
        models.PsychologicalInventoryQuestion,
        models.PsychologicalInventoryAnswer,
        models.PsychologicalInventorySummary,
    ]
)

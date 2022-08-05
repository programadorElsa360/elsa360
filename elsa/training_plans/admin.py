from django.contrib import admin

import elsa.training_plans.models as models

# Register your models here.
admin.site.register(
    [
        models.TrainingPlan,
        models.QuestionsToPlan,
        models.CyclingPlan,
        models.PhysicPlan,
        models.PhysicExerciseDescription,
    ]
)

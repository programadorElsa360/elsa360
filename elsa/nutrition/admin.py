from django.contrib import admin

import elsa.nutrition.models as models

# Register your models here.
admin.site.register(
    [models.FoodGroup, models.Food, models.MealSummary, models.FoodGroupIntake]
)

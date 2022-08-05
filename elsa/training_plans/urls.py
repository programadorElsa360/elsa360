from django.urls import path

from . import views


urlpatterns = [
    path(
        "training/daily/",
        views.DailyTrainingPlansView.as_view(),
        name="training_daily",
    ),
    path(
        "training/complete/",
        views.CompleteTrainingPlanView.as_view(),
        name="training_complete",
    ),
]

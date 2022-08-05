from django.urls import path

from rest_framework import routers

from . import views
from . import viewsets


router = routers.SimpleRouter()
router.register("users", viewsets.UserViewSet, basename="users")

urlpatterns = [
    path(r"login/", views.LoginView.as_view(), name="knox_login"),
    path(
        r"verify-user/<str:uidb64>/<str:token>/",
        views.VerifyUserView.as_view(),
        name="user_verify",
    ),
    path(
        "password-reset/request-email/",
        views.RequestPasswordResetView.as_view(),
        name="pwd_reset_email",
    ),
    path(
        "password-reset/verify/<str:uidb64>/<str:token>/",
        views.ConfirmPasswordResetView.as_view(),
        name="pwd_reset_verify",
    ),
    path(
        "password-reset/",
        views.PerformPasswordResetView.as_view(),
        name="password_reset",
    ),
]

urlpatterns += router.urls

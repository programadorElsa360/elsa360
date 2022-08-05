"""elsa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path

from elsa.memberships import urls as membership_urls
from elsa.nutrition import urls as nutrition_urls
from elsa.psychology import urls as psychology_urls
from elsa.training_plans import urls as training_plans_urls
from elsa.users import urls as user_urls

from knox import views as knox_views

from rest_framework.schemas import get_schema_view


urlpatterns = [
    path("admin/", admin.site.urls),
    path(r"logout/", knox_views.LogoutView.as_view(), name="knox_logout"),
    path(
        r"logoutall/",
        knox_views.LogoutAllView.as_view(),
        name="knox_logoutall",
    ),
    path("o/", include("oauth2_provider.urls", namespace="oauth2_provider")),
    path(
        r"openapi/",
        get_schema_view(
            title="ELSA",
            description="API for all things …",
            version="1.0.0",
        ),
        name="openapi-schema",
    ),
]

urlpatterns += user_urls.urlpatterns
urlpatterns += membership_urls.urlpatterns
urlpatterns += nutrition_urls.urlpatterns
urlpatterns += psychology_urls.urlpatterns
urlpatterns += training_plans_urls.urlpatterns

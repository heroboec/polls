from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/auth/token/",
        ObtainAuthToken.as_view(renderer_classes=[JSONRenderer, BrowsableAPIRenderer]),
        name="auth-token",
    ),
    path("api/", include("apps.core.urls")),
]

if settings.DEBUG and not settings.TESTING:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]

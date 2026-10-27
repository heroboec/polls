from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/token/", obtain_auth_token, name="auth-token"),
    path("api/", include("apps.core.urls")),
]

if settings.DEBUG and not settings.TESTING:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]

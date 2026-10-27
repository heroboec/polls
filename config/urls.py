from django.conf import settings
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.core.urls")),
]

if settings.DEBUG and not settings.TESTING:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]

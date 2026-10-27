from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import FooBar

router = DefaultRouter()

urlpatterns = [
    path("foobar/", FooBar.as_view(), name="health"),
    *router.urls,
]

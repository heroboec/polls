from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import FooBar, NextQuestionView, PollListView, PollStatisticView, UserChoiceView

router = DefaultRouter()

urlpatterns = [
    path("foobar/", FooBar.as_view(), name="health"),
    path("polls/", PollListView.as_view(), name="poll-list"),
    path("polls/<int:poll_id>/next-question/", NextQuestionView.as_view(), name="poll-next-question"),
    path("polls/<int:poll_id>/choices/", UserChoiceView.as_view(), name="poll-choices"),
    path("polls/<int:poll_id>/stats/", PollStatisticView.as_view(), name="poll-stats"),
    *router.urls,
]

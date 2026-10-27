from django.shortcuts import get_object_or_404

from apps.core.models import Poll, PollStatistic, State


def get_poll(poll_id):
    return get_object_or_404(Poll, pk=poll_id, is_active=True)


def get_or_start_state(poll, user):
    state, created = State.objects.get_or_create(
        poll=poll,
        user=user,
    )

    if created:
        statistic, _ = PollStatistic.objects.select_for_update().get_or_create(poll=poll)
        statistic.started += 1
        statistic.save()

    return state


def get_current_question(questions, state):
    position = state.answered_count
    return questions.order_by("sort_index", "id")[position:position + 1].first()

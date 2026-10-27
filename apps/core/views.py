from django.db import transaction
from django.db.models import Case, Exists, F, OuterRef, Value, When
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from apps.core.models import AnswerStatistic, Poll, PollStatistic, State
from apps.core.serializers import NextQuestionSerializer, PollListSerializer, UserChoicePostSerializer
from apps.core.utils import get_current_question, get_or_start_state, get_poll


class FooBar(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return JsonResponse({"FooBar": 1})


class PollListView(ListAPIView):
    serializer_class = PollListSerializer

    def get_queryset(self):
        states = State.objects.filter(poll=OuterRef("pk"), user=self.request.user)
        return Poll.objects.filter(is_active=True).annotate(
            status=Case(
                When(Exists(states.filter(stop_time__isnull=False)), then=Value("completed")),
                When(Exists(states), then=Value("in_progress")),
                default=Value("not_started"),
            ),
        ).order_by("-id")


class NextQuestionView(APIView):
    def get(self, request, poll_id):
        poll = get_poll(poll_id)

        with transaction.atomic():
            state = get_or_start_state(poll, request.user)

        questions = poll.questions.all()
        question = get_current_question(questions.prefetch_related('answers'), state)
        data = {
            "completed": question is None,
            "answered": state.answered_count,
            "total": questions.count(),
            "question": question,
        }
        return Response(NextQuestionSerializer(data).data)


class UserChoiceView(APIView):
    def post(self, request, poll_id):
        poll = get_poll(poll_id)
        serializer = UserChoicePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        answer = serializer.validated_data["answer"]

        with transaction.atomic():
            state = get_or_start_state(poll, request.user)

            answered = state.answered_count
            questions = poll.questions.all()
            question = get_current_question(questions, state)

            if question is None:
                return Response({"detail": "Опрос уже пройден"}, status=status.HTTP_400_BAD_REQUEST)

            # работаем только с ответами на этот вопрос
            if answer.question_id != question.id:
                return Response(
                    {"answer": "Вариант не относится к текущему вопросу"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # за один заход волшебство update
            updated = State.objects.filter(pk=state.pk, answered_count=answered).update(
                answered_count=F("answered_count") + 1,
            )
            # 0 строк: параллельный запрос уже принял ответ на этот вопрос и сдвинул прогресс
            if not updated:
                return Response({"detail": "Ответ на этот вопрос уже принят"}, status=status.HTTP_409_CONFLICT)

            serializer.save(question=question, poll_state=state)

            answer_statistic, _ = AnswerStatistic.objects.select_for_update().get_or_create(answer=answer)
            answer_statistic.choices_count += 1
            answer_statistic.save()

            total = questions.count()
            is_completed = answered + 1 == total
            if is_completed:
                # тут пишем, что прошли опрос
                state.stop_time = timezone.now()
                state.save(update_fields=["stop_time"])

                statistic, _ = PollStatistic.objects.select_for_update().get_or_create(poll=poll)
                statistic.completed += 1
                statistic.total_duration_sec += int((state.stop_time - state.start_time).total_seconds())
                statistic.save()

        return Response(
            {},
            status=status.HTTP_201_CREATED,
        )


class IsEditor(BasePermission):
    def has_permission(self, request, view):
        profile = getattr(request.user, "profile", None)
        return request.user.is_superuser or (profile is not None and profile.is_editor)


class PollStatisticView(APIView):
    permission_classes = [IsAuthenticated, IsEditor]

    def get(self, request, poll_id):
        get_object_or_404(Poll, pk=poll_id)
        return Response({})


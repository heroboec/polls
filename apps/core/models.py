from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q

from apps.core.mixins import CreatedMixin, UpdatedMixin

User = get_user_model()


class Poll(CreatedMixin, UpdatedMixin, models.Model):
    title = models.CharField(
        verbose_name='Название опроса',
        max_length=200,
        blank=False,
        null=False,
        default='',
    )

    author = models.ForeignKey(
        User,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )


class Question(models.Model):
    poll = models.ForeignKey(
        Poll,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )

    title = models.CharField(
        verbose_name='Текст вопроса',
        max_length=250,
        blank=False,
        null=False,
        default='',
    )

    sort_index = models.PositiveIntegerField(
        verbose_name='Индекс сортировки',
        blank=False,
        null=False,
        default=1,
    )


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )

    title = models.CharField(
        verbose_name='Вариант ответа',
        max_length=200,
        blank=False,
        null=False,
        default='',
    )

    sort_index = models.PositiveIntegerField(
        verbose_name='Индекс сортировки',
        blank=False,
        null=False,
        default=1,
    )

    is_open_answer = models.BooleanField(
        verbose_name='Это вопрос со свободным ответом',
        default=False,
    )


class State(models.Model):
    start_time = models.DateTimeField(
        verbose_name='Время начала опроса',
        auto_now_add=True,
        blank=False,
        null=False,
    )

    stop_time = models.DateTimeField(
        verbose_name='Время окончания опроса',
        blank=True,
        null=True,
    )

    user = models.ForeignKey(
        User,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )

    poll = models.ForeignKey(
        Poll,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )

    last_question_index = models.IntegerField(
        verbose_name='Индекс последнего отвеченного вопроса',
        blank=False,
        null=False,
        default=0,
    )

    class Meta:
        # запрещяем проходить один опрос дважды
        constraints = [
            models.UniqueConstraint(
                fields=['poll', 'user'],
                name='poll_user_uniq',
            ),
        ]


class UserChoice(models.Model):
    question = models.ForeignKey(
        Question,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )

    answer = models.ForeignKey(
        Answer,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )

    poll_state = models.ForeignKey(
        State,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )

    answer_text = models.CharField(
        verbose_name='Открытый ответ пользователя',
        max_length=100,
        null=True,
        blank=True,
        default=None,
    )

    class Meta:
        # запрещяем давать два ответа на один вопрос одному пользаку (неявно)
        constraints = [
            models.UniqueConstraint(
                fields=['poll_state', 'question'],
                name='question_user_uniq',
            ),
        ]
        # тут сможем поиметь список свободных ответов
        indexes = [
            models.Index(
                fields=['question'],
                name='userchoice_open_answers_idx',
                condition=Q(answer_text__isnull=False),
            ),
        ]


class PollStatistic(models.Model):
    poll = models.OneToOneField(
        Poll,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )

    started = models.PositiveIntegerField(
        verbose_name='Начато раз',
        default=0,
    )

    completed = models.PositiveIntegerField(
        verbose_name='Закончено раз',
        default=0,
    )

    total_duration_sec = models.PositiveBigIntegerField(
        'Сумма времен прохождения этого опроса',
        default=0,
    )


class AnswerStatistic(models.Model):
    answer = models.OneToOneField(
        Answer,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )

    choices_count = models.PositiveIntegerField(
        verbose_name='Сколько раз выбрали этот ответ',
        default=0,
    )




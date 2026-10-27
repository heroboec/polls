from django.db import models


class CreatedMixin(models.Model):
    created_at = models.DateTimeField(
        verbose_name='Время создания',
        null=False,
        blank=False,
        auto_now_add=True,
    )

    class Meta:
        abstract = True


class UpdatedMixin(models.Model):
    updated_at = models.DateTimeField(
        verbose_name='Время изменения',
        null=False,
        blank=False,
        auto_now=True,
    )

    class Meta:
        abstract = True


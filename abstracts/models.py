from django.db import models

class AbstractDateTime(models.Model):
    datetime_created = models.DateTimeField(
        verbose_name='Время создания',
        auto_now_add=True
    )
    datetima_updated = models.DateTimeField(
        verbose_name='Время редактирования',
        auto_now=True
    )
    datetime_deleted = models.DateTimeField(
        verbose_name='Время удаления',
        null=True,
        blank=True
    )

    class Meta:
        abstract = True

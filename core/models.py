from django.db import models
from django.contrib.auth.models import User, Group


class ProcessModel(models.Model):
    """Process"""

    class Meta:
        verbose_name = "Процесс"
        verbose_name_plural = "Процессы"

    name_ru = models.CharField(max_length=50, unique=True)
    name_en = models.CharField(max_length=50, unique=True)
    camunda_id = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name_ru


class TaskModel(models.Model):
    """Task"""

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    name = models.CharField(max_length=100)
    process = models.ForeignKey(
        ProcessModel,
        on_delete=models.SET_NULL,
        null=True,
    )
    responsible = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    responsible_group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

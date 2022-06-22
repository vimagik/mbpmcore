from django.db import models
from django.contrib.auth.models import User


class CmProcessContext(models.Model):

    class Meta:
        verbose_name = 'Поручение'
        verbose_name_plural = 'Поручения'

    short_name = models.CharField(max_length=100)
    what_to_do = models.CharField(max_length=500)
    responsible = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='responsible'
    )
    initiator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )
    perform_before = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.short_name



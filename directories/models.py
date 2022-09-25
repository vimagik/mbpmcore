from django.db import models
from django.contrib.auth.models import User


class Meeting(models.Model):
    """Model for meetings"""

    class Meta:
        verbose_name = 'Встреча'
        verbose_name_plural = 'Встречи'

    name = models.CharField(max_length=50)
    due_of_event = models.DateField()
    description = models.TextField()
    participants = models.ManyToManyField(User)

    def __str__(self):
        return self.name


class Arrangement(models.Model):

    class Meta:
        verbose_name = 'Договоренность'
        verbose_name_plural = 'Договоренности'

    description = models.TextField()
    create_date = models.DateField(auto_now_add=True)
    meeting = models.ForeignKey(
        Meeting,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.description[:10]}... на встрече {self.meeting.name}'

from django.db import models

from tracker.models import Tasks


class Employee(models.Model):

    fio = models.CharField(max_length=200, verbose_name="ФИО сотрудника")
    employee_position = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Должность"
    )
    tasks = models.ManyToManyField(Tasks, blank=True, verbose_name="Задачи")

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return self.fio

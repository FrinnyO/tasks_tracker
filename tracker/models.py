from django.db import models


class Tasks(models.Model):
    STATUS_CHOICE = [
        ("inactive", "Не активна"),
        ("active", "В работе"),
        ("complete", "Выполнена"),
    ]
    title = models.CharField(max_length=100, verbose_name="Название")
    related_task = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        verbose_name="Связанная родительская задача",
        blank=True,
        null=True,
    )
    time = models.CharField(blank=True, null=True, verbose_name="Срок выполнения")
    status = models.CharField(
        max_length=100,
        choices=STATUS_CHOICE,
        default="inactive",
        blank=True,
        null=True,
        verbose_name="Статус выполнения",
    )

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self):
        return self.title

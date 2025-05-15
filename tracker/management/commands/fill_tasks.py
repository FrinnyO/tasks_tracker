import csv
import random

import pandas as pd
from django.core.management.base import BaseCommand
from faker import Faker

fake = Faker()

num_records = 100


class Command(BaseCommand):
    def handle(self, *args, **options):
        statuses = ["Не активна", "В работе", "Выполнена"]

        data = {
            "ID задачи": [],
            "Название": [],
            "Связанная родительская задача": [],
            "Статус выполнения": [],
            "Срок выполнения": [],
            "Сотрудники": [],
            "Дата создания": [],
        }

        for task_id in range(1, num_records + 1):
            data["ID задачи"].append(task_id)
            data["Название"].append(fake.sentence(nb_words=6))
            data["Связанная родительская задача"].append(fake.text(max_nb_chars=200))
            data["Статус выполнения"].append(random.choice(statuses))
            data["Срок выполнения"].append(
                fake.date_between(start_date="today", end_date="+30d")
            )
            data["Сотрудники"].append(fake.name())
            data["Дата создания"].append(fake.date_this_year())

        df = pd.DataFrame(data)

        df["Связанная родительская задача"] = df["Связанная родительская задача"].str.replace(
            "\n", " "
        )

        df.to_csv(
            "task_tracker.csv",
            index=False,
            encoding="utf-8-sig",
            sep=";",
            quoting=csv.QUOTE_MINIMAL,
            quotechar='"',
            lineterminator="\n",
        )

        print("Таблица задач успешно заполнена и сохранена в 'task_tracker.csv'")

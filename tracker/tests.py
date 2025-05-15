from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Tasks


class TrackerTest(APITestCase):
    def setUp(self):
        Tasks.objects.all().delete()
        self.tasks = Tasks.objects.create(title="Test", time="2 дня")

    def test_tracker_create(self):
        data = {
            "title": "TESTtitle",
            "time": "TESTtime",
            "status": "active",
        }
        response = self.client.post("/tracker/", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tasks.objects.count(), 2)
        self.assertEqual(
            response.json(),
            {
                "id": 7,
                "title": "TESTtitle",
                "time": "TESTtime",
                "status": "active",
                "related_task": None,
            },
        )

    def test_tracker_list(self):
        url = reverse("tracker:tracker-list")
        response = self.client.get(url)
        data = response.json()
        print(data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            data,
            [
                {
                    "id": 9,
                    "title": "Test",
                    "time": "2 дня",
                    "status": "inactive",
                    "related_task": None,
                }
            ],
        )
        self.assertEqual(Tasks.objects.count(), 1)

    def test_tracker_retrieve(self):
        url = reverse("tracker:tracker-detail", args=(self.tasks.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            data,
            {
                "id": self.tasks.id,
                "title": "Test",
                "time": "2 дня",
                "status": "inactive",
                "related_task": None,
            },
        )

    def test_tracker_update(self):
        url = reverse("tracker:tracker-detail", args=(self.tasks.pk,))
        data = {
            "related_tracker": [self.tasks.id],
            "status": "inactive",
            "time": "TESTtime",
            "title": "TESTtitle",
        }
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Tasks.objects.count(), 1)
        self.assertEqual(response.json()["status"], "inactive")

    def test_tracker_delete(self):
        url = reverse("tracker:tracker-detail", args=(self.tasks.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tasks.objects.count(), 0)

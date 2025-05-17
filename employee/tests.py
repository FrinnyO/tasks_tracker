from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tracker.models import Tasks

from .models import Employee


class EmployeeTest(APITestCase):

    def setUp(self):
        Employee.objects.all().delete()
        Tasks.objects.all().delete()

        self.tasks = Tasks.objects.create(title="Test", time="2 дня")
        self.employee = Employee.objects.create(fio="Иванов Иван Иванович")

    def test_employee_create(self):
        data = {
            "fio": "TESTfio",
            "employee_position": "TESTpos",
        }
        response = self.client.post("/employee/", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Employee.objects.count(), 2)

        # Сверяем данные с ожидаемыми
        self.assertEqual(
            response.json(),
            {"employee_position": "TESTpos", "fio": "TESTfio", "id": 2, "tasks": []},
        )

    def test_employee_list(self):

        url = reverse("employee:employee-list")
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            data,
            [
                {
                    "id": self.employee.id,
                    "fio": "Иванов Иван Иванович",
                    "employee_position": None,
                    "tracker_count": 0,
                    "tasks": [],
                }
            ],
        )
        self.assertEqual(Employee.objects.count(), 1)

    def test_employee_retrieve(self):
        url = reverse("employee:employee-detail", args=(self.employee.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            data,
            {
                "id": self.employee.id,
                "fio": "Иванов Иван Иванович",
                "employee_position": None,
                "tracker_count": 0,
                "tasks": [],
            },
        )

    def test_employee_update(self):
        url = reverse("employee:employee-detail", args=(self.employee.pk,))
        data = {
            "fio": "TestUPDATE",
            "employee_position": "TESTUPDATE",
        }
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Employee.objects.count(), 1)
        self.assertEqual(response.json()["fio"], "TestUPDATE")

    def test_employee_delete(self):
        url = reverse("employee:employee-detail", args=(self.employee.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employee.objects.count(), 0)

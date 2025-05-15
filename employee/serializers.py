from rest_framework import serializers

from employee.models import Employee
from tracker.serializers import TasksSerializer


class EmployeeSerializer(serializers.ModelSerializer):

    tracker_count = serializers.IntegerField(read_only=True)
    tasks = TasksSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = ["id", "fio", "employee_position", "tracker_count", "tasks"]

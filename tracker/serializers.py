from rest_framework import serializers

from tracker.models import Tasks


class TasksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tasks
        fields = "__all__"

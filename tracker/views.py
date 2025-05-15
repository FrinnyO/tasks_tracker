from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from tracker.filters import TrackerFilter
from tracker.models import Tasks
from tracker.serializers import TasksSerializer


class TrackerViewset(viewsets.ModelViewSet):

    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = TrackerFilter
    ordering_fields = ("id", "status")

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        filter_params = request.query_params
        if filter_params.get("important_trackers") == "true":
            formated_response = []
            for item in serializer.data:
                formated_response.append(
                    {
                        "Важная задача": item["title"],
                        "Срок выполнения": item["time"],
                    }
                )
            return Response(formated_response)
        return Response(serializer.data)

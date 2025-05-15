import django_filters
from django.db.models import Q

from tracker.models import Tasks


class TrackerFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name="status", lookup_expr="exact")
    related_task_isnull = django_filters.BooleanFilter(
        field_name="related_task", lookup_expr="isnull"
    )
    related_task_status = django_filters.CharFilter(
        field_name="related_task__status", lookup_expr="exact"
    )
    important_task = django_filters.BooleanFilter(method="filter_important_task")

    class Meta:
        model = Tasks
        fields = [
            "status",
            "related_task_isnull",
            "related_task_status",
            "important_task",
        ]

    def filter_important_task(self, queryset, name, value):
        status_check = queryset.filter(status="inactive")
        related_task_check = queryset.filter(related_task__isnull=False)
        related_task_status_check = queryset.filter(related_task__status="active")
        return queryset.filter(
            Q(pk__in=status_check)
            & Q(pk__in=related_task_check)
            & Q(pk__in=related_task_status_check)
        )

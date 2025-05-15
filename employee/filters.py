import django_filters
from django.db.models import Count, Min

from employee.models import Employee


class EmployeeFilter(django_filters.FilterSet):
    count_lte = django_filters.NumberFilter(
        field_name="tracker_count", lookup_expr="lte"
    )
    count_gte = django_filters.NumberFilter(
        field_name="tracker_count", lookup_expr="gte"
    )
    can_take_task = django_filters.BooleanFilter(method="filter_can_take_task")

    class Meta:
        model = Employee
        fields = ("count_lte", "count_gte", "can_take_task")

    def filter_can_take_task(self, queryset, name, value):
        min_tracker_count = queryset.annotate(
            tracker_count=Count("trackers")
        ).aggregate(Min("tracker_count"))["tracker_count__min"]
        possible_employees = queryset.filter(tracker_count__lte=min_tracker_count + 2)
        parent_tasks_employees = queryset.filter(
            trackers__related_tracker__isnull=False
        )
        return queryset.filter(pk__in=parent_tasks_employees | possible_employees)

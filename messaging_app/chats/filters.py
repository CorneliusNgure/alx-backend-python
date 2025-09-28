import django_filters
from .models import Message


class MessageFilter(django_filters.FilterSet):
    """
    Filter messages by user (sender or recipient) and by time range.
    """
    user = django_filters.NumberFilter(
        field_name="sender__user_id", lookup_expr="exact"
    )
    recipient = django_filters.NumberFilter(
        field_name="recipient__user_id", lookup_expr="exact"
    )
    start_date = django_filters.DateTimeFilter(
        field_name="sent_at", lookup_expr="gte"
    )
    end_date = django_filters.DateTimeFilter(
        field_name="sent_at", lookup_expr="lte"
    )

    class Meta:
        model = Message
        fields = ["user", "recipient", "start_date", "end_date"]
from django.db.models import Prefetch, F, Sum
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.clients.models import Client
from apps.services.models import Subscription, Plan
from apps.services.serializers import SubscriptionSerializer, PlanSerializer


class SubscriptionView(ReadOnlyModelViewSet):
    serializer_class = SubscriptionSerializer

    queryset = Subscription.objects.prefetch_related(
        "plan",
        Prefetch(
            "client",
            queryset=Client.objects.select_related("user").only(
                "company_name", "user__email"
            ),
        ),
    ).annotate(
        price=F("service__full_price")
        - (F("service__full_price") * F("plan__discount_percent") / 100.0)
    )

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        response_data = {
            "result": response.data,
            "total_price": self.queryset.aggregate(total_price=Sum("price")).get(
                "total_price"
            ),
        }
        response.data = response_data

        return response


class PlanView(ReadOnlyModelViewSet):
    serializer_class = PlanSerializer
    queryset = Plan.objects.all()

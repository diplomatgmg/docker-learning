from django.conf import settings
from django.core.cache import cache
from django.db.models import Prefetch, Sum
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
    )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)

        price_cache = cache.get(settings.PRICE_CACHE_NAME)

        if price_cache:
            total_price = price_cache
        else:
            total_price = queryset.aggregate(total_price=Sum("price")).get(
                "total_price"
            )
            cache.set(settings.PRICE_CACHE_NAME, total_price, 60)

        response_data = {
            "result": response.data,
            "total_price": total_price
        }
        response.data = response_data

        return response


class PlanView(ReadOnlyModelViewSet):
    serializer_class = PlanSerializer
    queryset = Plan.objects.all()

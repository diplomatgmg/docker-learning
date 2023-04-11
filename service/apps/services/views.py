from django.db.models import Prefetch
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.clients.models import Client
from apps.services.models import Subscription, Plan
from apps.services.serializers import SubscriptionSerializer, PlanSerializer


class SubscriptionView(ReadOnlyModelViewSet):
    serializer_class = SubscriptionSerializer

    queryset = Subscription.objects.prefetch_related(
        'plan',
        Prefetch('client',
                 queryset=Client.objects.select_related('user').only('company_name',
                                                                     'user__email'))
    )


class PlanView(ReadOnlyModelViewSet):
    serializer_class = PlanSerializer
    queryset = Plan.objects.all()

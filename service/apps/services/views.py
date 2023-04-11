from django.db.models import Prefetch
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.clients.models import Client
from apps.services.models import Subscription
from apps.services.serializers import SubscriptionSerializer


class SubscriptionView(ReadOnlyModelViewSet):
    serializer_class = SubscriptionSerializer

    queryset = Subscription.objects.all().prefetch_related(
        Prefetch('client',
                 queryset=Client.objects.all().select_related('user').only(
                     'company_name', 'user__email'))
    )

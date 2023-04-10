from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.services.models import Subscription
from apps.services.serializers import SubscriptionSerializer


class SubscriptionView(ReadOnlyModelViewSet):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()

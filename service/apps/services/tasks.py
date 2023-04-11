from celery import shared_task
from django.db.models import F


@shared_task
def set_price(subscription_id):
    from apps.services.models import Subscription

    subscription = (
        Subscription.objects.filter(id=subscription_id)
        .annotate(
            annotated_price=F("service__full_price")
            - F("service__full_price") * F("plan__discount_percent") / 100.00
        )
        .first()
    )

    subscription.price = subscription.annotated_price
    subscription.save()
    return 10

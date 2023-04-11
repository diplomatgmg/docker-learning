from rest_framework import serializers

from apps.services.models import Subscription, Plan


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ("plan", "client_name", "email", "price")

    plan = PlanSerializer()
    client_name = serializers.CharField(source="client.company_name")

    email = serializers.EmailField(source="client.user.email")
    price = serializers.SerializerMethodField()

    # def get_price(self, instance: Subscription):
    #     full_price = instance.service.full_price
    #     return full_price - full_price * (instance.plan.discount_percent / 100)

    def get_price(self, instance: Subscription):
        return instance.price

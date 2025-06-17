from rest_framework import serializers
from pools.models import GiftPool, Donation


class GiftPoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiftPool
        fields = ['id', 'title', 'description', 'occasion', 'target_amount', 'current_amount', 'created_at']

class DonationSerializer(serializers.ModelSerializer):
    donor = serializers.StringRelatedField()

    class Meta:
        model = Donation
        fields = ['amount', 'donated_at', 'donor']
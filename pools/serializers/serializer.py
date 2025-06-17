from rest_framework import serializers
from pools.models import GiftPool

class GiftPoolSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = GiftPool
        fields = ['id', 'title', 'description', 'occasion', 'target_amount', 'current_amount', 'created_at']

    def get_id(self, obj):
        return str(obj.id)

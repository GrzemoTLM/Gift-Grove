from rest_framework import serializers
from pools.models import GiftPool, Donation, PoolInvitation
from users.models import AppUser


class AppUserSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    
    class Meta:
        model = AppUser
        fields = ['id', 'username', 'email']
    
    def get_id(self, obj):
        return str(obj.id) if obj.id else None


class GiftPoolSerializer(serializers.ModelSerializer):
    owner = AppUserSerializer(read_only=True)
    invited_users = serializers.SerializerMethodField()
    
    class Meta:
        model = GiftPool
        fields = ['id', 'title', 'description', 'occasion', 'target_amount', 'current_amount', 'created_at', 'owner', 'invited_users']
    
    def get_invited_users(self, obj):
        return AppUserSerializer(obj.get_invited_users(), many=True).data


class DonationSerializer(serializers.ModelSerializer):
    donor = AppUserSerializer(read_only=True)
    id = serializers.SerializerMethodField()

    class Meta:
        model = Donation
        fields = ['id', 'amount', 'donated_at', 'donor']
    
    def get_id(self, obj):
        return str(obj.id) if obj.id else None


class PoolInvitationSerializer(serializers.ModelSerializer):
    invited_user = AppUserSerializer(read_only=True)
    invited_by = AppUserSerializer(read_only=True)
    pool_title = serializers.CharField(source='pool.title', read_only=True)
    id = serializers.SerializerMethodField()
    
    class Meta:
        model = PoolInvitation
        fields = ['id', 'pool', 'pool_title', 'invited_user', 'invited_by', 'accepted', 'created_at', 'accepted_at']
    
    def get_id(self, obj):
        return str(obj.id) if obj.id else None


class CreatePoolInvitationSerializer(serializers.ModelSerializer):
    invited_username = serializers.CharField(write_only=True)
    
    class Meta:
        model = PoolInvitation
        fields = ['invited_username']
    
    def validate_invited_username(self, value):
        try:
            user = AppUser.objects.get(username=value)
            return user
        except AppUser.DoesNotExist:
            raise serializers.ValidationError("User with this username does not exist.")
    
    def create(self, validated_data):
        invited_user = validated_data.pop('invited_username')
        pool = self.context['pool']
        invited_by = self.context['invited_by']
        
        invitation, created = PoolInvitation.objects.get_or_create(
            pool=pool,
            invited_user=invited_user,
            defaults={'invited_by': invited_by}
        )
        
        if not created:
            raise serializers.ValidationError("Invitation already exists for this user.")
        
        return invitation
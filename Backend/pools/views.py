from django.shortcuts import get_object_or_404
from django.db import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils import timezone

from users.models import AppUser
from .models import GiftPool, Donation, PoolInvitation
from decimal import Decimal
from pools.serializers.serializer import (
    GiftPoolSerializer, DonationSerializer, PoolInvitationSerializer, 
    CreatePoolInvitationSerializer, AppUserSerializer
)


class CreateGiftPoolView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GiftPoolSerializer(data=request.data)
        if serializer.is_valid():
            payload = request.auth.payload
            username = payload.get("username")
            user = get_object_or_404(AppUser, username=username)
            gift_pool = serializer.save(owner=user)
            return Response(GiftPoolSerializer(gift_pool).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListGiftPoolsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        payload = request.auth.payload
        username = payload.get("username")
        user = get_object_or_404(AppUser, username=username)

        accessible_pools = GiftPool.objects.filter(
            models.Q(owner=user) | 
            models.Q(invitations__invited_user=user, invitations__accepted=True)
        ).distinct()
        
        serializer = GiftPoolSerializer(accessible_pools, many=True)
        return Response(serializer.data)


class DonateToGiftPoolView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pool_id):
        amount = request.data.get("amount")

        if not amount:
            return Response({"error": "Missing amount"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            return Response({"error": "Invalid amount"}, status=status.HTTP_400_BAD_REQUEST)

        pool = get_object_or_404(GiftPool, id=pool_id)
        payload = request.auth.payload
        username = payload.get("username")
        user = get_object_or_404(AppUser, username=username)
        
        if not pool.is_accessible_by(user):
            return Response({"error": "You don't have access to this pool"}, status=status.HTTP_403_FORBIDDEN)
        
        amount = Decimal(str(amount))
        pool.current_amount += amount
        pool.save()

        donation = Donation(
            pool=pool,
            donor=user,
            amount=amount
        )
        donation.save()

        return Response({"message": "Donation successful", "new_total": pool.current_amount}, status=200)


class PoolDonationsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pool_id):
        pool = get_object_or_404(GiftPool, id=pool_id)

        payload = request.auth.payload
        username = payload.get("username")
        user = get_object_or_404(AppUser, username=username)
        
        if not pool.is_accessible_by(user):
            return Response({"error": "You don't have access to this pool"}, status=status.HTTP_403_FORBIDDEN)
        
        donations = pool.donations.all().order_by("-donated_at")
        serializer = DonationSerializer(donations, many=True)
        return Response(serializer.data)


class DonationHistoryView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pool_id):
        pool = get_object_or_404(GiftPool, id=pool_id)

        payload = request.auth.payload
        username = payload.get("username")
        user = get_object_or_404(AppUser, username=username)
        
        if not pool.is_accessible_by(user):
            return Response({"error": "You don't have access to this pool"}, status=status.HTTP_403_FORBIDDEN)
        
        donations = Donation.objects.filter(pool=pool).order_by("-donated_at")
        serializer = DonationSerializer(donations, many=True)
        return Response(serializer.data, status=200)


class InviteUserToPoolView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pool_id):
        pool = get_object_or_404(GiftPool, id=pool_id)

        payload = request.auth.payload
        username = payload.get("username")
        user = get_object_or_404(AppUser, username=username)
        
        if pool.owner != user:
            return Response({"error": "Only the pool owner can invite users"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = CreatePoolInvitationSerializer(
            data=request.data,
            context={'pool': pool, 'invited_by': user}
        )
        
        if serializer.is_valid():
            invitation = serializer.save()
            return Response(
                PoolInvitationSerializer(invitation).data, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AcceptPoolInvitationView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, invitation_id):
        invitation = get_object_or_404(PoolInvitation, id=invitation_id)
        payload = request.auth.payload
        username = payload.get("username")
        user = get_object_or_404(AppUser, username=username)
        
        if invitation.invited_user != user:
            return Response({"error": "You can only accept your own invitations"}, status=status.HTTP_403_FORBIDDEN)
        
        if invitation.accepted:
            return Response({"error": "Invitation already accepted"}, status=status.HTTP_400_BAD_REQUEST)
        
        invitation.accepted = True
        invitation.accepted_at = timezone.now()
        invitation.save()
        
        return Response({"message": "Invitation accepted successfully"}, status=200)


class ListMyInvitationsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        payload = request.auth.payload
        username = payload.get("username")
        user = get_object_or_404(AppUser, username=username)
        
        invitations = PoolInvitation.objects.filter(invited_user=user, accepted=False)
        serializer = PoolInvitationSerializer(invitations, many=True)
        return Response(serializer.data)


class ListDonationsView:
    pass


class EditGiftPoolView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, pool_id):
        pool = get_object_or_404(GiftPool, id=pool_id)
        payload = request.auth.payload
        username = payload.get("username")
        if pool.owner.username != username:
            return Response({"error": "Only the owner can edit this pool"}, status=status.HTTP_403_FORBIDDEN)
        serializer = GiftPoolSerializer(pool, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteGiftPoolView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pool_id):
        pool = get_object_or_404(GiftPool, id=pool_id)
        payload = request.auth.payload
        username = payload.get("username")
        if pool.owner.username != username:
            return Response({"error": "Only the owner can delete this pool"}, status=status.HTTP_403_FORBIDDEN)
        pool.delete()
        return Response({"message": "Pool deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
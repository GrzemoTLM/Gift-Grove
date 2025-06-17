from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.models import AppUser
from .models import GiftPool, Donation
from decimal import Decimal
from pools.serializers.serializer import GiftPoolSerializer, DonationSerializer


class CreateGiftPoolView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GiftPoolSerializer(data=request.data)
        if serializer.is_valid():
            gift_pool = serializer.save()
            return Response(GiftPoolSerializer(gift_pool).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListGiftPoolsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        gift_pools = GiftPool.objects.all()
        serializer = GiftPoolSerializer(gift_pools, many=True)
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
        amount = Decimal(str(amount))
        pool.current_amount += amount
        pool.save()

        # Get user from JWT payload
        payload = request.auth.payload
        username = payload.get("username")
        user = get_object_or_404(AppUser, username=username)
        
        # Debug: Check if user is saved
        print(f"User ID: {user.id}, User PK: {user.pk}, User saved: {user.pk is not None}")
        print(f"Username: {username}, User object: {user}")

        # Create donation without trying to save the user object
        donation = Donation(
            pool=pool,
            donor=user,
            amount=amount
        )
        donation.save()

        return Response({"message": "Donation successful", "new_total": pool.current_amount}, status=200)

class PoolDonationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pool_id):
        pool = get_object_or_404(GiftPool, id=pool_id)
        donations = pool.donations.all().order_by("-donated_at")
        serializer = DonationSerializer(donations, many=True)
        return Response(serializer.data)

class DonationHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pool_id):
        pool = get_object_or_404(GiftPool, id=pool_id)
        donations = Donation.objects.filter(pool=pool).order_by("-donated_at")
        serializer = DonationSerializer(donations, many=True)
        return Response(serializer.data, status=200)


class ListDonationsView:
    pass
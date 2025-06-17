from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import GiftPool
from decimal import Decimal
from pools.serializers.serializer import GiftPoolSerializer

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
        amount = Decimal(str(request.data.get("amount")))
        pool.current_amount += amount
        pool.save()

        return Response({"message": "Donation successful", "new_total": pool.current_amount}, status=200)
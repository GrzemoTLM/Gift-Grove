from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import GiftPool
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

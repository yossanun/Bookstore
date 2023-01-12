from .utils import CustomPagination
from .serializers import TransactionSerializer, TransactionCreateSerializer
from .models import Book, Transaction, Configuration
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response


class TransactionView(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    pagination_class = CustomPagination
    
    action_serializers = {
        'create': TransactionCreateSerializer
    }

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'): 
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]

        return super().get_serializer_class()

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        book = Book.objects.filter(id=request.data.get('book')).first()
        serializer = self.get_serializer(data=request.data)
        is_use_cash = request.data.get('is_use_cash', False)
        is_use_point = request.data.get('is_use_point', False)
        serializer.is_valid(raise_exception=True)
        transaction = serializer.save()
        transaction.add_point = book.point
        promotion_config = Configuration.objects.filter(name='promotion-1').first()
        price_config = Configuration.objects.filter(name='price-1').first()  # price_config.value ค่า point สำหรับ config

        # ----- Configuration Point -----
        if is_use_cash and transaction.use_cash > price_config.value:  # ทุก ๆ  100 บาท จะได้ promotion_config.value พ้อย
            transaction.add_point += (transaction.use_cash // price_config.value) * promotion_config.value
        transaction.save()

        member = transaction.member

        # ----- Calculate Transaction -----

            # ------ Use cash and point -----
        if is_use_cash and is_use_point:
            point = transaction.use_point
            cash = transaction.use_cash
            total = point + cash
            if total < book.price:
                return Response({'message': 'Cash is not enough.'}, status=status.HTTP_400_BAD_REQUEST)

            member.point += transaction.add_point

            # ------ Use Cash -----
        elif is_use_cash:
            if int(request.data.get('use_cash')) < book.price:
                return Response({'message': 'Cash is not enough.'}, status=status.HTTP_400_BAD_REQUEST)

            member.point += transaction.add_point
        
            # ------ Redeem Point -----
        elif is_use_point:
            if member.point < transaction.use_point:
                return Response({'message': 'Point is not enough.'}, status=status.HTTP_400_BAD_REQUEST)

            member.point -= transaction.use_point

        member.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        if pk:
            obj = self.get_object()
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(self.filter_queryset(self.get_queryset()), status=status.HTTP_404_NOT_FOUND)
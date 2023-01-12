from .serializers import AuthorSerializer
from .models import Author
from .utils import CustomPagination

from rest_framework import status, viewsets, mixins
from rest_framework.response import Response


class AuthorView(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class = CustomPagination

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None):
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        serializer.save()

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        if pk:
            obj = self.get_object()
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(self.filter_queryset(self.get_queryset()), status=status.HTTP_404_NOT_FOUND)
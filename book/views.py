from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination

from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated

from .models import Book
from .serializers import BookSerializer


class BookPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "count"
    max_page_size = 5000
    page_query_param = "page"


class BookListCreateView(generics.ListCreateAPIView):
    serializer_class = BookSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    pagination_class = BookPagination

    filterset_fields = ["id", "title", "authors"]
    search_fields = ("id", "title", "authors")
    ordering_fields = ("id", "title", "authors")


    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Book.objects.filter(owner=self.request.user)


class BookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def get_queryset(self):
        return Book.objects.filter(owner=self.request.user)
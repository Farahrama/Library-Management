from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Book
from .serializers import BookSerializer

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["isbn"]
    search_fields = ["title", "author", "isbn"]
    ordering_fields = ["title", "published_date", "copies_available"]

    def get_queryset(self):
        qs = super().get_queryset()
        available = self.request.query_params.get("available")
        if available is not None:
            if available.lower() in ["true", "1", "yes"]:
                qs = qs.filter(copies_available__gt=0)
            elif available.lower() in ["false", "0", "no"]:
                qs = qs.filter(copies_available__lte=0)
        return qs

    @action(detail=False, methods=["get"], url_path="stats")
    def stats(self, request):
        total = Book.objects.count()
        available = Book.objects.filter(copies_available__gt=0).count()
        return Response({"total": total, "available": available})
# Create your views here.

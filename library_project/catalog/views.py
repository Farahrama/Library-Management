from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db import transaction as db_txn
from rest_framework import viewsets, permissions, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied
from .models import Book, Transaction
from .serializers import BookSerializer, TransactionSerializer, UserSerializer

User = get_user_model()


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        return bool(request.user and request.user.is_staff)


class BookViewSet(viewsets.ModelViewSet):
    """
    - GET list/retrieve للجميع (public read)
    - POST/PUT/PATCH/DELETE للـ admin فقط
    - فلترة + بحث + Pagination
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = {
        "isbn": ["exact"],
        "published_date": ["exact", "year__exact"],
        "copies_available": ["gte", "lte", "exact"],
    }
    search_fields = ["title", "author", "isbn"]
    ordering_fields = ["title", "author", "published_date", "copies_available"]

    @action(detail=False, methods=["get"], url_path="available")
    def available(self, request):
        """عرض الكتب المتاحة فقط (copies_available > 0)"""
        qs = self.get_queryset().filter(copies_available__gt=0)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(self.get_serializer(qs, many=True).data)

    @action(detail=True, methods=["post"], url_path="checkout", permission_classes=[permissions.IsAuthenticated])
    def checkout(self, request, pk=None):
        """
        قواعد:
        - لازم يكون فيه نسخ متاحة
        - نفس المستخدم ما يقدرش يمسك نفس الكتاب مرتين في نفس الوقت
        - يتم تقليل copies_available
        """
        book = self.get_object()
        user = request.user

        if book.copies_available <= 0:
            raise ValidationError("No available copies for this book.")

        # تأكد إنه ما عندوش checkout نشط لنفس الكتاب
        if Transaction.objects.filter(user=user, book=book, return_date__isnull=True).exists():
            raise ValidationError("You already have an active checkout for this book.")

        with db_txn.atomic():
            # قفل تشاركي بسيط عبر الترتيب (اختياري لو DB تدعم select_for_update)
            book = Book.objects.select_for_update().get(pk=book.pk)
            if book.copies_available <= 0:
                raise ValidationError("No available copies for this book.")
            # أنشئ المعاملة وقلل النسخ
            Transaction.objects.create(user=user, book=book)
            book.copies_available -= 1
            book.save(update_fields=["copies_available"])

        return Response({"detail": "Book checked out successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="return", permission_classes=[permissions.IsAuthenticated])
    def return_book(self, request, pk=None):
        """
        - لازم يكون للمستخدم Checkout نشط لهذا الكتاب
        - احسب return_date وزوّد copies_available
        """
        book = self.get_object()
        user = request.user

        tx = Transaction.objects.filter(user=user, book=book, return_date__isnull=True).first()
        if not tx:
            raise ValidationError("No active checkout found for this book.")

        with db_txn.atomic():
            tx.return_date = timezone.now()
            tx.save(update_fields=["return_date"])

            book = Book.objects.select_for_update().get(pk=book.pk)
            book.copies_available += 1
            book.save(update_fields=["copies_available"])

        return Response({"detail": "Book returned successfully."}, status=status.HTTP_200_OK)


class MyTransactionsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    المستخدم يشوف تاريخه فقط.
    /api/my/transactions/
    """
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).select_related("book")


# (اختياري) إدارة المستخدمين للـ admin
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    search_fields = ["username", "email"]
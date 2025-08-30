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
from django.shortcuts import render
from .models import Book

def book_list_view(request):
    books = Book.objects.all()
    return render(request, 'books_list.html', {'books': books})
from django.contrib.auth.decorators import login_required

@login_required
def checkout_view(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        try:
            book = Book.objects.get(id=book_id)
            if book.copies_available > 0:
                book.copies_available -= 1
                book.save()
                Borrowing.objects.create(user=request.user, book=book)
                return render(request, 'checkout.html', {'message': 'تمت الإعارة بنجاح!'})
            else:
                return render(request, 'checkout.html', {'error': 'الكتاب غير متاح.'})
        except Book.DoesNotExist:
            return render(request, 'checkout.html', {'error': 'الكتاب غير موجود.'})
    return render(request, 'checkout.html')
from django.utils import timezone

@login_required
def return_view(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        try:
            book = Book.objects.get(id=book_id)
            borrowing = Borrowing.objects.filter(user=request.user, book=book, return_date__isnull=True).first()
            if borrowing:
                borrowing.return_date = timezone.now()
                borrowing.save()
                book.copies_available += 1
                book.save()
                return render(request, 'return.html', {'message': 'تم إرجاع الكتاب بنجاح!'})
            else:
                return render(request, 'return.html', {'error': 'لم يتم إعارة هذا الكتاب بواسطتك.'})
        except Book.DoesNotExist:
            return render(request, 'return.html', {'error': 'الكتاب غير موجود.'})
    return render(request, 'return.html')
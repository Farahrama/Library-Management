from rest_framework import serializers
from .models import Book
from datetime import date
from api.models import Book, Borrowing


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'published_date', 'copies_available']

    def validate_published_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("تاريخ النشر لا يمكن أن يكون في المستقبل")
        return value

class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ['id', 'user', 'book', 'borrow_date', 'return_date']
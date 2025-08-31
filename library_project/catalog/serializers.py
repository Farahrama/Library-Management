from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Book, Transaction
from datetime import date
User = get_user_model()




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_active", "date_joined"]
        read_only_fields = ["date_joined"]
from rest_framework import serializers
from .models import Book, Borrowing

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
class TransactionSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ["id", "book", "checkout_date", "return_date", "is_active"]

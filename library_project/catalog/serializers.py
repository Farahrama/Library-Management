from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Book, Transaction

User = get_user_model()


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author", "isbn", "published_date", "copies_available"]


class TransactionSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ["id", "book", "checkout_date", "return_date", "is_active"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_active", "date_joined"]
        read_only_fields = ["date_joined"]
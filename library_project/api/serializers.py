from rest_framework import serializers
from .models import Book
from datetime import date

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author", "isbn", "published_date", "copies_available"]
        read_only_fields = ["id"]

    def validate_published_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("تاريخ النشر لا يمكن أن يكون في المستقبل.")
        return value

    def validate_copies_available(self, value):
        if value < 0:
            raise serializers.ValidationError("عدد النسخ المتاحة لا يمكن أن يكون سالبًا.")
        return value

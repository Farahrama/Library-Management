from django.conf import settings
from django.db import models
from django.db.models import Q


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)  # Unique ISBN
    published_date = models.DateField(null=True, blank=True)
    copies_available = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} ({self.isbn})"


class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="transactions")
    checkout_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "book"],
                condition=Q(return_date__isnull=True),
                name="unique_active_checkout_per_user_book",
            )
        ]
        ordering = ["-checkout_date"]

    @property
    def is_active(self):
        return self.return_date is None

    def __str__(self):
        return f"{self.user} -> {self.book} | active={self.is_active}"
# Create your models here.

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, MyTransactionsViewSet, UserViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'my/transactions', MyTransactionsViewSet, basename='my-transactions')
router.register(r'users', UserViewSet, basename='user')  # Admin only

urlpatterns = [
    path('', include(router.urls)),
]
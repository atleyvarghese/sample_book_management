from django.conf.urls import url, include
from rest_framework import routers

from apps.books.views import BorrowBookAPIView, BorrowedBooksAPIView
from apps.common.views import UserViewSet, CustomAuthToken

router = routers.DefaultRouter()
router.register(r'^users', UserViewSet)

urlpatterns = [
    url(r'^v1/', include(router.urls)),
    url(r'^v1/api-token-auth/', CustomAuthToken.as_view()),
    url(r'^v1/borrow-book/$', BorrowBookAPIView.as_view(), name='borrow-book'),
    url(r'^v1/borrowed-books/$', BorrowedBooksAPIView.as_view(), name='borrowed-books'),
]

import datetime

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.books.models import Book, BorrowedBooks
from apps.books.serializers import BookListSerializer


class BorrowBookAPIView(APIView):

    def post(self, request):
        response = {}
        if self.request.data.get('book_id') and self.request.data.get('date'):
            try:
                book = Book.objects.get(id=self.request.data.get('book_id'))
            except Book.DoesNotExist:
                response = {
                    'book_id' : "Invalid Book ID"
                }
                return Response(response, 400)
            try:
                date = datetime.datetime.strptime(self.request.data.get('date'), '%Y-%m-%d')
            except ValueError:
                response = {
                    'date': "Invalid date"
                }
                return Response(response, 400)

            if book.available_stock > 0:
                book.available_stock = book.available_stock - 1
                book.save()
                BorrowedBooks.objects.create(user=request.user, book=book, borrowed_date=date)
                response['book_id'] = "Successfully Registered"
            else:
                response = {
                    'book_id': "Book is currently not available"
                }
                return Response(response, 400)
        else:
            response = {
                'book_id': "required",
                'date': "required"
            }
            return Response(response, 400)
        return Response(response, 200)


class BorrowedBooksAPIView(generics.ListAPIView):
    serializer_class = BookListSerializer

    def get_queryset(self):
        return Book.objects.filter(id__in=self.request.user.borrowed_books.all().values_list('book_id')).distinct()

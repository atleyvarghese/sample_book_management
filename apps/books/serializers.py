from rest_framework import serializers

from apps.books.models import Book


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('title', 'author')

from django.contrib import admin

from apps.books.models import Book


class BookAdmin(admin.ModelAdmin):
    ordering = ('-created_at',)
    search_fields = ['title', 'author']
    list_display = ['title', 'author', 'available_stock', ]


admin.site.register(Book, BookAdmin)

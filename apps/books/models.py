from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Book(models.Model):
    title = models.CharField(verbose_name='Title', max_length=250)
    author = models.CharField(verbose_name='Author', max_length=250)
    available_stock = models.PositiveIntegerField(verbose_name='Available Stock', default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")

    def __str__(self):
        return '{} by {}'.format(self.title, self.author)


class BorrowedBooks(models.Model):
    user = models.ForeignKey(User, related_name='borrowed_books', on_delete=models.SET_NULL, null=True)
    book = models.ForeignKey(Book, related_name='borrowed_users', on_delete=models.SET_NULL, null=True)

    returned = models.BooleanField(default=False)
    borrowed_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Borrowed Book")
        verbose_name_plural = _("Borrowed Books")

    def __str__(self):
        return '{} borrowed {} on {}'.format(self.user.email, self.book.title, self.created_at)

>>> from bookshelf.models import Book
>>> book = Book.objects.first()
>>> book.delete()
(1, {'bookshelf.Book': 1})
>>> Book.objects.all()
<QuerySet []>


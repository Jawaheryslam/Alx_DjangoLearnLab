from django.shortcuts import render
from .models import Book
from django.db.models import Q

def search_books(request):
    query = request.Get.get('q', '')
    books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
    return render(request, 'bookshelf/book_list.html', {'books': books})

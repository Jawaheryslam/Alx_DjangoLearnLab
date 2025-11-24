from django.shortcuts import render, redirect
from .models import Book
from .forms import ExampleForm
from django.db.models import Q

def example_view(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('book_list')
        else:
            form = ExampleForm()
            return render(request, 'bookshelf/form_example.html', {'form': form})

def search_books(request):
    query = request.Get.get('q', '')
    books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
    return render(request, 'bookshelf/book_list.html', {'books': books})

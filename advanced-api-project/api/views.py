from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
    """
    retrieves all books
    Accessible for both authenitcated and unauthenticated users
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookDetailView(generics.RetrieveAPIView):
    """
    retrieves a single book by Id
    Read-only access for all users
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    """
    adds a new book
    restricted to authenticated users only
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        cyustomize create behaviour
        ensure validation data is properly saved
        """

        publication_year = serializer.validation_data.get('publication_year')

        if publication_year < 1900:
            raise ValidationError(
                    {"publication_year": "Books published before 1900 are not allowed."}
            )

        serializer.save()



class BookUpdateView(generics.UpdateAPIView):
    """
    modifies an existing book
    restricted to authenticated users only
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        """
        customize update behaviour
        ensures updated data remains valid
        """

        publication_year = serializer.validated_data.get('publication_year')

        if publication_year and publication_year < 1900:
            raise ValidationError(
                    {"publication_year": "Invalid publication year."}
            )

        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    """
    removes a book
    restricted to authenticated users only
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


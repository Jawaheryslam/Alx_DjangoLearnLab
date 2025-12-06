from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from api.models import Author, Book


class BookAPITestCase(APITestCase):
    """
    test case for book api CRUD operations,
    filterinf, searching, ordering and permissions,
    """

    def setUp(self):
        """
        set up test data befroe each test.
        """

        self.user = User.objects.create_user(
                username='testuser',
                password='testpassword'
        )

        self.author = Author.objects.create(name="Ngugi wa Thiong'o")

        self.book1 = Book.objects.create(
                title="Petals of Blood",
                publication_year=1977,
                author=self.author
        )

        self.book2 = Book.objects.create(
                title="A Grain of Wheat",
                publication_year=1967,
                author=self.author
        )

        self.book_list_url = "/api/books/"
        self.book_create_url = "/api/books/create/"
        self.book_update_url = f"/api/books/update/{self.book1.id}/"
        self.book_delete_url = f"/api/books/delete/{self.book1.id}/"

    # Read tests(public access)
    def test_list_books(self):
        """
        test retrieving all books
        """

        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # create tests
    def test_create_book_authentiated(self):  # test with authentication
        self.client.login(username='testuser', password='testpassword')

        data = {
                "title": "Devil on the Cross",
                "publication_year": 1980,
                "author": self.author.id
        }

        response = self.client.post(self.book_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_create_book_unauthenticated(self):  # test without authentication
        data = {
                "title": "Unauthorized Book",
                "publication_year": 2000,
                "author": self.author.id
        }

        response = self.client.post(self.book_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # update tests
    def test_update_book_authenticated(self):  # test updating a book with authentication
        self.client.login(username="testuser", password="testpassword")

        data = {
                "title": "Petals of Blood (Updated)",
                "publication_year": 1978,
                "author": self.author.id
        }

        response = self.client.put(self.book_update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # delete tests
    def test_delete_book_authenticated(self):  # test deleting a book with authentication
        self.client.login(username="testuser", password="testpassword")

        response = self.client.delete(self.book_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    # filtering tests
    def test_filter_books_by_year(self):  # test filtering books by publication year
        response = self.client.get(self.book_list_url + "?publication_year=1977")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


    # search tests
    def test_search_books_by_title(self):  # test searching books by title
        response = self.client.get(self.book_list_url + "?search=Grain")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertequal(len(response.data), 1)


    # ordering tests
    def test_order_books_by_publication_year(self):  # test ordering books by publication year
        response = self.client.get(self.book_list_url + "?ordering=publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
                response.data[0]["publication_year"],
                1967
        )


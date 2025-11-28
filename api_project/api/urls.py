from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import BookList, BookViewSet

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
        # Route for the Booklist view(ListAPIView)
        path('books/', BookList.as_view(), name='book-list'),

        path('api-token-auth/', obtain_auth_token, name='api-token-auth'),


        # Include the router urls for BookViewSet (all CRUD operations)
        path('', include(router.urls)),  # This includes all routes registered with the router
]

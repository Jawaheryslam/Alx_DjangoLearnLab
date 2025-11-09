from django.urls import path
from .views import list_books, LibraryDetailView, register
from django.contrib.auth import Login, Logout

urlpatterns = [
        path('books/', views.list_books, name='list_books'),
        path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),

        #Authentication
        path('register/', register, name='register'),
        path('login/', Login.as_view(template_name='relationship_app/login.html'), name='login'),
        path('logout/', Logout.as_view(template_name='relationship_app/logout.html'), name='logout'),
]

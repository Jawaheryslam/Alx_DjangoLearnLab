from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
        path('login/', views.CustomLoginView.as_view(), name='login'),
        path('logout/', views.CustomLogoutView.as_view(), name='logout'),
        path('register/', views.register, name='register'),
        path('profile/', views.profile, name='profile'),
        path('posts/', views.PostListview.as_view(), name='post-list'),
        path('posts/new/', views.PostCreateView.as_view(), name='post-create'),
        path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
        path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_update'),
        path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
]

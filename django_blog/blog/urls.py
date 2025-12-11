from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
        path('login/', views.CustomLoginView.as_view(), name='login'),
        path('logout/', views.CustomLogoutView.as_view(), name='logout'),
        path('register/', views.register, name='register'),
        path('profile/', views.profile, name='profile'),
        path('posts/', views.PostListview.as_view(), name='post-list'),
        path('post/new/', views.PostCreateView.as_view(), name='post-create'),
        path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
        path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
        path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
        path('', views.PostListView.as_view(), name='post-list'),
]

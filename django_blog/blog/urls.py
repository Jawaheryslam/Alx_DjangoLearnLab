from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
        # posts
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

        # comments
        path('post/<int:pk>/comment/new', views.CommentCreateView.as_view(), name='comment-create'),
        path('post/<int:pk>/comments/new/', views.add_comment, name='add_comment'),
        path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment-update'),
        path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),

        # tags & search
        path('tags/<str:tag_name>/', views.PostsByTagListView.as_view(), name='posts-by-tag'),
        path('search/', views.SearchResultsView.as_view(), name='search-results'),
]

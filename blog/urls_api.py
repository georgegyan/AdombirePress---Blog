from django.urls import path
from . import views

# API URLs only
urlpatterns = [
    path('categories/', views.CategoryListCreateView.as_view(), name='api-category-list'),
    path('categories/<slug:slug>/', views.CategoryDetailView.as_view(), name='api-category-detail'),
    path('posts/', views.PostListView.as_view(), name='api-post-list'),
    path('posts/<slug:slug>/', views.PostDetailView.as_view(), name='api-post-detail'),
    path('posts/<slug:post_slug>/comments/', views.CommentListCreateView.as_view(), name='api-comment-list'),
    path('comments/<int:pk>/', views.CommentDetailView.as_view(), name='api-comment-detail'),
    path('posts/<slug:post_slug>/like/', views.LikeCreateView.as_view(), name='api-post-like'),
    path('posts/<slug:post_slug>/likes-count/', views.post_likes_count, name='api-post-likes-count'),
]
from django.urls import path, include
from . import views

urlpatterns = [
    # Category URLs
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<slug:slug>/', views.CategoryDetailView.as_view(), name='category-detail'),
    
    # Post URLs
    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('posts/create/', views.PostCreateView.as_view(), name='post-create'),
    path('posts/<slug:slug>/', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/<slug:slug>/edit/', views.PostUpdateDeleteView.as_view(), name='post-edit'),
    
    # Comment URLs
    path('posts/<slug:post_slug>/comments/', views.CommentListCreateView.as_view(), name='comment-list'),
    path('comments/<int:pk>/', views.CommentDetailView.as_view(), name='comment-detail'),
    
    # Like URLs
    path('posts/<slug:post_slug>/like/', views.LikeCreateView.as_view(), name='post-like'),
    path('posts/<slug:post_slug>/likes-count/', views.post_likes_count, name='post-likes-count'),
]
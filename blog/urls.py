from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Template URLs
    path('', views.home, name='home'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/<slug:slug>/', views.post_detail, name='post_detail'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<slug:slug>/', views.category_posts, name='category_posts'),

    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Keep API URLs (they won't interfere)
    path('api/categories/', views.CategoryListCreateView.as_view(), name='api-category-list'),
    path('api/categories/<slug:slug>/', views.CategoryDetailView.as_view(), name='api-category-detail'),
    path('api/posts/', views.PostListView.as_view(), name='api-post-list'),
    path('api/posts/<slug:slug>/', views.PostDetailView.as_view(), name='api-post-detail'),

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
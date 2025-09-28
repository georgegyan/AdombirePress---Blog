from django.db.models import Q  # Add this import
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Count
from .models import Category, Post, Comment, Like
from .serializers import (
    CategorySerializer, PostListSerializer, PostDetailSerializer,
    PostCreateUpdateSerializer, CommentSerializer, LikeSerializer
)
from .permissions import IsAdminOrReadOnly

class CategoryListCreateView(generics.ListCreateAPIView):
    """
    View to list all categories or create a new category
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def get_queryset(self):
        # Annotate with post count for each category
        return Category.objects.annotate(
            post_count=Count('posts', filter=Q(posts__status='published'))  # Fixed: use Q instead of models.Q
        )

class PostListView(generics.ListAPIView):
    """
    View to list all published posts
    """
    serializer_class = PostListSerializer
    
    def get_queryset(self):
        queryset = Post.objects.filter(status='published').select_related('author', 'category')
        
        # Filter by category if provided
        category_slug = self.request.query_params.get('category', None)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Search functionality
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(content__icontains=search) |
                Q(excerpt__icontains=search)
            )
        
        return queryset
    
from django.db.models import Q, Count  # Fixed import
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Category, Post, Comment, Like
from .serializers import (
    CategorySerializer, PostListSerializer, PostDetailSerializer,
    PostCreateUpdateSerializer, CommentSerializer, LikeSerializer
)
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly

class CategoryListCreateView(generics.ListCreateAPIView):
    """
    View to list all categories or create a new category
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def get_queryset(self):
        # Annotate with post count for each category
        return Category.objects.annotate(
            post_count=Count('posts', filter=Q(posts__status='published'))
        )

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update or delete a category
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'

class PostListView(generics.ListAPIView):
    """
    View to list all published posts
    """
    serializer_class = PostListSerializer
    
    def get_queryset(self):
        queryset = Post.objects.filter(status='published').select_related('author', 'category')
        
        # Filter by category if provided
        category_slug = self.request.query_params.get('category', None)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Search functionality
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(content__icontains=search) |
                Q(excerpt__icontains=search)
            )
        
        return queryset

class PostDetailView(generics.RetrieveAPIView):
    """
    View to retrieve a single post
    """
    queryset = Post.objects.filter(status='published')
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'

class PostCreateView(generics.CreateAPIView):
    """
    View to create a new post
    """
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to update or delete a post (author only)
    """
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostDetailSerializer
        return PostCreateUpdateSerializer

class CommentListCreateView(generics.ListCreateAPIView):
    """
    View to list comments for a post or create a new comment
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        post_slug = self.kwargs['post_slug']
        return Comment.objects.filter(
            post__slug=post_slug, 
            is_approved=True
        ).select_related('author', 'post')
    
    def perform_create(self, serializer):
        post_slug = self.kwargs['post_slug']
        post = Post.objects.get(slug=post_slug)
        serializer.save(post=post, author=self.request.user)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update or delete a comment
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

class LikeCreateView(generics.CreateAPIView):
    """
    View to like/unlike a post
    """
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        post_slug = kwargs['post_slug']
        post = Post.objects.get(slug=post_slug)
        user = request.user
        
        # Check if user already liked this post
        existing_like = Like.objects.filter(post=post, user=user).first()
        
        if existing_like:
            # Unlike - remove the like
            existing_like.delete()
            return Response({"detail": "Post unliked"}, status=status.HTTP_200_OK)
        else:
            # Like - create new like
            serializer = self.get_serializer(data={
                'post': post.id,
                'reaction': request.data.get('reaction', 'like')
            })
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def post_likes_count(request, post_slug):
    """
    View to get like count and reactions for a post
    """
    try:
        post = Post.objects.get(slug=post_slug)
        likes = Like.objects.filter(post=post)
        
        data = {
            'total_likes': likes.count(),
            'reactions': {
                'like': likes.filter(reaction='like').count(),
                'love': likes.filter(reaction='love').count(),
                'laugh': likes.filter(reaction='laugh').count(),
                'wow': likes.filter(reaction='wow').count(),
            }
        }
        return Response(data)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
    
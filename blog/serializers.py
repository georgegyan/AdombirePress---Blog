from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Post, Comment, Like

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model
    """
    post_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'created_at', 'post_count']
        read_only_fields = ['id', 'slug', 'created_at', 'post_count']
    
    def get_post_count(self, obj):
        """Get count of published posts in this category"""
        return obj.posts.filter(status='published').count()
    
class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model
    """
    author_name = serializers.CharField(source='author.username', read_only=True)
    post_title = serializers.CharField(source='post.title', read_only=True)
    
    class Meta:
        model = Comment
        fields = [
            'id', 'post', 'post_title', 'author', 'author_name', 'content', 
            'is_approved', 'parent', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # Set the author to the current user
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
    
class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer for Like/Reaction model
    """
    user_name = serializers.CharField(source='user.username', read_only=True)
    post_title = serializers.CharField(source='post.title', read_only=True)
    
    class Meta:
        model = Like
        fields = ['id', 'post', 'post_title', 'user', 'user_name', 'reaction', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
    
    def create(self, validated_data):
        # Set the user to the current user
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
class PostListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing posts (shorter version)
    """
    author_name = serializers.CharField(source='author.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    comment_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'excerpt', 'featured_image', 'author', 'author_name',
            'category', 'category_name', 'status', 'created_at', 'comment_count', 'like_count'
        ]
        read_only_fields = ['id', 'slug', 'created_at']
    
    def get_comment_count(self, obj):
        return obj.comments.filter(is_approved=True).count()
    
    def get_like_count(self, obj):
        return obj.likes.count()

class PostDetailSerializer(PostListSerializer):
    """
    Serializer for detailed post view (includes full content and comments)
    """
    comments = CommentSerializer(many=True, read_only=True)
    category_detail = CategorySerializer(source='category', read_only=True)
    
    class Meta(PostListSerializer.Meta):
        fields = PostListSerializer.Meta.fields + [
            'content', 'published_at', 'meta_title', 'meta_description', 
            'comments', 'category_detail'
        ]

class PostCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating posts
    """
    class Meta:
        model = Post
        fields = [
            'title', 'content', 'excerpt', 'featured_image', 'category', 
            'status', 'meta_title', 'meta_description'
        ]
    
    def create(self, validated_data):
        # Set the author to the current user
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
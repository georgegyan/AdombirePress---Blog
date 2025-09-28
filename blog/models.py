from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class Category(models.Model):
    """
    Model for organizing posts into categories (Tech, Lifestyle, News, etc.)
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category-posts', kwargs={'slug': self.slug})
    
class Post(models.Model):
    """
    Main blog post model
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique_for_date='created_at')
    content = models.TextField()
    excerpt = models.TextField(max_length=300, blank=True, help_text="Brief summary of the post")
    featured_image = models.ImageField(upload_to='posts/%Y/%m/%d/', blank=True)
    
    # Relationships
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    
    # Metadata
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    # SEO fields
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(max_length=300, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at', 'status']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        """Auto-set published_at when status changes to published"""
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})
    
class Comment(models.Model):
    """
    Comments on blog posts
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_comments')
    content = models.TextField(max_length=1000)
    is_approved = models.BooleanField(default=False)  # Moderation feature
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Optional: Reply functionality
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.author} on {self.post}"
    
class Like(models.Model):
    """
    Track likes/reactions on posts
    """
    REACTION_CHOICES = [
        ('like', '👍 Like'),
        ('love', '❤️ Love'),
        ('laugh', '😄 Laugh'),
        ('wow', '😲 Wow'),
    ]
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_likes')
    reaction = models.CharField(max_length=10, choices=REACTION_CHOICES, default='like')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['post', 'user']  # One reaction per user per post
    
    def __str__(self):
        return f"{self.user} reacted {self.reaction} to {self.post}"
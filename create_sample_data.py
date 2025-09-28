import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adombire_press.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Category, Post

# Create sample users
admin_user = User.objects.create_superuser('admin', 'admin@adombire.com', 'adminpass')
author1 = User.objects.create_user('john', 'john@adombire.com', 'johnpass')
author2 = User.objects.create_user('sarah', 'sarah@adombire.com', 'sarahpass')

# Create categories
tech_category = Category.objects.create(name='Technology', slug='technology', description='Tech news and reviews')
lifestyle_category = Category.objects.create(name='Lifestyle', slug='lifestyle', description='Lifestyle and culture')
news_category = Category.objects.create(name='News', slug='news', description='Current events')

# Create sample posts
post1 = Post.objects.create(
    title='Welcome to Adombire Press',
    slug='welcome-to-adombire-press',
    content='This is the first post on our new blog platform...',
    excerpt='A warm welcome to our new blogging platform',
    author=admin_user,
    category=tech_category,
    status='published'
)

post2 = Post.objects.create(
    title='The Future of Web Development',
    slug='future-of-web-development',
    content='Web development is evolving rapidly with new frameworks...',
    excerpt='Exploring the latest trends in web development',
    author=author1,
    category=tech_category,
    status='published'
)

post3 = Post.objects.create(
    title='Healthy Living Tips',
    slug='healthy-living-tips',
    content='Maintaining a healthy lifestyle is important for...',
    excerpt='Simple tips for a healthier lifestyle',
    author=author2,
    category=lifestyle_category,
    status='published'
)

print("Sample data created successfully!")
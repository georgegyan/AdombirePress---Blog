from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    # Redirect root to home page
    path('', RedirectView.as_view(url='/blog/', permanent=False)),
    
    # Blog app URLs (templates)
    path('blog/', include('blog.urls')),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # Keep API URLs (they won't interfere)
    path('api/blog/', include('blog.urls_api')),
    path('api/users/', include('users.urls')),
    path('api-auth/', include('rest_framework.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
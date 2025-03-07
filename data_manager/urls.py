from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    # Home page that lists available golf files
    path('', views.file_list, name='file_list'),
    
    # Dynamic URL to download a specific file
    path('download/<str:file_name>/', views.download_file, name='download_file'),
    
    # Endpoint to fetch golf data (top golfers)
    path('fetch_golf_data/', views.fetch_golf_data, name='fetch_golf_data'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
